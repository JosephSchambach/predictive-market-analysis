import pandas as pd
import numpy as np

class NaiveForecast:
    def __init__(self, data, forecast_steps: int):
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
        
    def lookback(self):
        try: 
            self.lookback_data = self.data['close'][:self.forecast_steps]
        except Exception as e:
            raise ValueError(f"An error occurred extracting the data: {str(e)}")
        
    def forecast(self):
        for i in range(self.forecast_steps):
            next_date = self.data['date'].max() + pd.offsets.BDay(1)
            next_value = self.lookback_data.iloc[-(i+1)]
            new_row = pd.DataFrame({'date': [next_date], 'close': [next_value]})
            self.data = pd.concat([self.data, new_row], ignore_index=True)
    
    def format_and_return(self):
        self.data = self.data.sort_values(by='date', ascending=True)
        return self.data
    
    def run(self):
        try:
            self.lookback()
            self.forecast()
            self.format_and_return()
            return self.data
        except Exception as e:
            raise ValueError(f"An error occurred forecasting the data: {str(e)}")