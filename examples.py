from context import MarketPredictorContext
from api.alpha_vantage_api import *
from models.AlphaVantage import get_function
import requests 
import json

context = MarketPredictorContext()

# from the user
symbol = input("Enter a symbol: ")
timeframe = input("Enter a timeframe: ")
# behind the scenes
# stock = context.api.execute('stock_symbol_search', symbol=symbol)
function = get_function(timeframe)
result = context.api.execute('fetch_stock_prices', function=function, symbol=symbol)
print(result.head())
pass