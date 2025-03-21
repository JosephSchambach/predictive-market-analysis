from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller, acf, pacf
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
import math

class ArimaModel:
    def __init__(self, data: pd.DataFrame, forecast_steps: int):
        self.data = data if 'date' in data.columns and 'close' in data.columns else None
        if self.data is None:
            raise ValueError("Data must have a date column")
        self.forecast_steps = forecast_steps
        self._preprocess_data()

    def _preprocess_data(self):
        try: 
            self.data['close'] = self.data['close'].astype(float)
            self.data['date'] = pd.to_datetime(self.data['date'])
            self.data = self.data.sort_values(by='date', ascending=False)
        except Exception as e:
            raise ValueError(f"An error occurred preparing the data: {str(e)}")
        
    def auto_diff(self):
        df = self.data.copy()
        for i in range(0, 5):
            if adfuller(df['close'].dropna())[1] < 0.05:
                return i
            df['close'] = df['close'].diff()
        return 6

    def auto_correlation_handler(self, data: np.array):
        if len(data) < 2:
            raise ValueError("Data must have at least 2 values")
        num_lags = []
        for conf_int in data[1]:
            if conf_int[0] > 0.5:
                num_lags.append(conf_int[0])
            else:
                break
        return len(num_lags) - 1

    def auto_lag(self):
        data = self.data['close']
        nlags = round(math.sqrt(len(data)),0)
        pacf_vals = pacf(data.dropna(), nlags=nlags, alpha=0.05)
        return self.auto_correlation_handler(pacf_vals)


    def auto_ma(self):
        data = self.data['close']
        nlags = round(math.sqrt(len(data)),0)
        acf_vals = acf(data.dropna(), nlags=nlags, alpha=0.05)
        return self.auto_correlation_handler(acf_vals)

    def forecast(self, model):
        try:
            model = model.fit()
            forecast = model.forecast(steps=self.forecast_steps)
            return forecast
        except Exception as e:
            raise ValueError(f"An error occurred forecasting the data: {str(e)}")
    
    def format_and_return(self, forecast):
        self.data = self.data.sort_values(by='date', ascending=True)
        for value in forecast:
            next_date = self.data['date'].max() + pd.offsets.BDay(1)
            next_value = value
            new_row = pd.DataFrame({'date': [next_date], 'close': [next_value]})
            self.data = pd.concat([self.data, new_row], ignore_index=True)
        return self.data

    def run(self):
        diff= self.auto_diff()
        if diff == 6:
            raise ValueError("Data could not be differenced")
        try:
            lag = self.auto_lag()
            moving_avg = self.auto_ma()
        except Exception as e:
            raise ValueError(f"An error occurred determining the lag and moving average: {str(e)}")
        close_prices = self.data['close'].sort_index(ascending=True)
        model = ARIMA(close_prices, order=(lag, diff, moving_avg))
        forecast_values = self.forecast(model)
        return self.format_and_return(forecast_values)