from context import Context
import requests 
import json

context = Context()

symbol = "AAPL"

result = context.api._alpha_vantage.get_daily(symbol)

pass