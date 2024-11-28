from context import MarketPredictorContext
from api.alpha_vantage_api import *
from models.AlphaVantage import get_function
from analysis.technical_indicators import moving_average
from matplotlib import pyplot as plt
from api import dashboard_api
import requests 
import json

context = MarketPredictorContext()
data = context.api.execute('file_read', file='result.csv')
# data.drop(['50_day_moving_average', '25_day_moving_average', 'spread'], axis=1, inplace=True)
# print(data)
# data.to_csv("result.csv", index=False)
# from the user

symbol = input("Enter a symbol: ")
timeframe = input("Enter a timeframe: ")
while timeframe.replace(' ','') == "dailyadjusted" or timeframe == 'daily_adjusted': 
    timeframe = input("This is a premium feature. Enter a timeframe: ")
# behind the scenes
stock = context.api.execute('stock_symbol_search', symbol=symbol)

result = context.api.execute('fetch_stock_prices', timeframe=timeframe, symbol=symbol)
result = moving_average(result, [50,200], 'close')
print(result.head())

context.api.execute('plot', data=result,x='date', y=['close','50_day_moving_average', '200_day_moving_average'])
pass
