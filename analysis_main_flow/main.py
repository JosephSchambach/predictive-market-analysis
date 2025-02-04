from predictive_market_analysis.context.predictor_context import MarketPredictorContext
from predictive_market_analysis.database.database_config import *
from predictive_market_analysis.analysis.technical_indicators import moving_average
from predictive_market_analysis.ml_model.neural_network import LSTMModel
import pandas as pd

context = MarketPredictorContext()

class MainFlowHandler():
    def __init__(self, context):
        self.context = context
    
    def run(self):
        context.logger.log('Starting the main flow')

        self.ticker = input("Enter a ticker: ")
        self.timeframe = input("Enter a timeframe: ")
        self.api_data_raw = context.api.execute('fetch_stock_prices', symbol=self.ticker, timeframe=self.timeframe)

        self.api_data_cleaned = self.api_data_raw[['date', 'close']]

        context.database.insert('apple_data_raw', self.api_data_cleaned)

        self.data_from_db = context.database.select('apple_data_raw', ['date', 'close'])

        forecast = context.model.forecast(LSTMModel(data=self.data_from_db,forecast_steps=2,lookback=8))

        context.database.upsert('apple_data_raw', forecast)
        pass

if __name__ == '__main__':
    handler = MainFlowHandler(context)
    handler.run()