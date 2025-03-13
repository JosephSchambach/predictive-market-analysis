import pandas as pd
from pandas.tseries.offsets import BDay
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import torch
from torch import nn
from torch.optim import Adam

class LSTMModel():
    def __init__(self, data, forecast_steps: int, lookback: int, epochs: int = 50):
        self.data = data if 'date' in data.columns and 'close' in data.columns else None
        if self.data is None:
            raise ValueError("Data must have a date column")
        self.forecast_steps = forecast_steps
        self.lookback = lookback
        self.epochs = epochs
        self.sequences = self._preprocess_data(data)

    def _preprocess_data(self, df: pd.DataFrame):
        try:
            df['close'] = df['close'].astype(float)
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
            close = df.close
            close_values = close.to_numpy()

            self.scaler = MinMaxScaler(feature_range=(-1, 1))
            data = self.scaler.fit_transform(close_values.reshape(-1, 1))

            sequences = []
            for index in range(len(data) - (self.forecast_steps + self.lookback)):
                sequences.append(data[index:index + (self.forecast_steps + self.lookback)])
            sequences = np.array(sequences)
            return sequences
        except Exception as e:
            raise ValueError(f"An error occurred preparing the data: {str(e)}")

    def train_test_split(self, sequences: np.array):
        try: 
            valid_set_percentage = 0.2

            valid_set_size = int(np.round(valid_set_percentage*sequences.shape[0]))
            train_set_size = sequences.shape[0] - valid_set_size

            x_train = sequences[:train_set_size, :-(self.forecast_steps), :]
            y_train = sequences[:train_set_size, -self.forecast_steps:, :]
            x_valid = sequences[train_set_size:train_set_size+valid_set_size, :-(self.forecast_steps), :]
            y_valid = sequences[train_set_size:train_set_size+valid_set_size, -self.forecast_steps:, :]

            self.x_train = torch.from_numpy(x_train).type(torch.Tensor)
            self.y_train = torch.from_numpy(y_train).type(torch.Tensor)
            self.x_valid = torch.from_numpy(x_valid).type(torch.Tensor)
            self.y_valid = torch.from_numpy(y_valid).type(torch.Tensor)
        except Exception as e: 
            raise ValueError(f"An error occurred splitting the data into training and testing sets: {str(e)}")

    def model_train(self): 
        hist = np.zeros(self.epochs)
        for epoch in range(self.epochs):
            y_train_pred = self.model(self.x_train)
            y_train_flat = self.y_train.view(y_train_pred.shape)
            loss = self.mse(y_train_pred, y_train_flat)

            if epoch % 10 == 0:
                print(f'Epoch {epoch} - Training Loss: {loss.item()}')

            hist[epoch] = loss.item()
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def forecast(self):
        self.model.eval()
        last_sequence = self.x_valid[-1:] 
        
        with torch.no_grad():
            forecast = self.model(last_sequence)
        
        forecast = self.scaler.inverse_transform(forecast.cpu().numpy())
        return forecast.squeeze()

    def format_response(self, forecast: np.array):
        last_date = self.data["date"].iloc[-1]
        next_dates = []
        for i in range(self.forecast_steps):
            next_dates.append(last_date + BDay(i+1))
        forecast_df = pd.DataFrame().from_dict(data={"date": next_dates,"close": forecast}, orient='columns')
        new_data = pd.concat([self.data, forecast_df], ignore_index=True)
        new_data['date'] = new_data['date'].dt.strftime('%Y-%m-%d')
        new_data['close'] = new_data['close'].round(2)
        return new_data

    def run(self): 
        self.train_test_split(self.sequences)
        model = LSTM(
            input_size=self.lookback,  
            hidden_dimensions=64, 
            num_layers=2, 
            output_size=self.forecast_steps
        )
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') 
        self.model = model.to(device)
        self.optimizer = Adam(model.parameters(),lr=0.01)
        self.mse = nn.MSELoss()
        self.model_train()
        _forecast = self.forecast()
        forecast = self.format_response(_forecast)
        return forecast

class LSTM(nn.Module): 
    def __init__(self, input_size, hidden_dimensions, num_layers, output_size):
        super(LSTM, self).__init__()
        self.hidden_dim = hidden_dimensions
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_dimensions, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dimensions, output_size)
    
    def forward(self, x): 
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()

        out, (hn, cn) = self.lstm(x, (h0.detach(), c0.detach()))
        out = self.fc(out[:, -1, :]) 
        return out