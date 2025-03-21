from predictive_ma.context.predictor_context import MarketPredictorContext
from predictive_ma.ml_model.naive_forecast import NaiveForecast
from predictive_ma.models.AlphaVantage import get_function
from matplotlib import pyplot as plt
from predictive_ma.api import dashboard_api
import pandas as pd
import requests 
import json
import math
from predictive_ma.database.etl_class import ETLClass
from predictive_ma.ml_model.arima_forecast import ArimaModel

context = MarketPredictorContext()
data = context.database.select('aapl_daily', ['date', 'close'])
forecast = context.model.forecast(ArimaModel(data, 5))


forecast = context.model.forecast(NaiveForecast(data, 5))

context.dashboard.layout('Stock Price Dashboard', subtitle='Interactive Dashboard: Change Stock Symbol and Timeframe and select Machine Learning Forecast parameters if desired')
context.dashboard.run()
# Plotting the data
plt.figure(figsize=(10, 5))
plt.plot(data['date'], data['close'], label='Close Price')
plt.xticks(data['date'][::100], rotation=45)
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title('Stock Close Price Over Time')
plt.legend()
plt.grid(True) 
plt.show()

data = context.api.execute('file_read', file='result.csv')
data = data[['date', 'close']]
context.database.insert('apple_data_raw', data)

data_from_sb = context.database.select('apple_data_raw', ['date', 'close'])
data_from_sb.loc[len(data_from_sb)] = ['2021-07-21', 110.0]
context.database.upsert('apple_data_raw', data_from_sb)


context.logger.log('Starting the test')
context.logger.log("This is a test", 'ERROR')
context.logger.log("This is a test", 'CRITICAL')

symbol = 'AAPL'
timeframe = 'daily'
result = context.api.execute('fetch_stock_prices', timeframe=timeframe, symbol=symbol)
data = ti.on_balance_volume(result, 'close')

data = context.api.execute('file_read', file='result.csv')
data.drop(['50_day_moving_average', '25_day_moving_average', 'spread'], axis=1, inplace=True)
print(data)
data.to_csv("result.csv", index=False)

# from the user
symbol = input("Enter a symbol: ")
timeframe = input("Enter a timeframe: ")
while timeframe.replace(' ','') == "dailyadjusted" or timeframe == 'daily_adjusted': 
    timeframe = input("This is a premium feature. Enter a timeframe: ")
# behind the scenes
stock = context.api.execute('stock_symbol_search', symbol=symbol)

result = ti.moving_average(result, [50,200], 'close')
print(result.head())

context.api.execute('plot', data=result,x='date', y=['close','50_day_moving_average', '200_day_moving_average'])
pass
