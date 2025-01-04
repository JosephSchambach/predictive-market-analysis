import requests
import json
import pandas as pd
from predictive_market_analysis.models.AlphaVantage import get_function

class AlphaVantageAPI: 
    def __init__(self, api_config, logger): 
        self.base_url = api_config['alpha_vantage_url'] + api_config['alpha_vantage_api_key']
        self.logger=logger

    def fetch_stock_prices(self, timeframe, symbol): 
        function_output = get_function(timeframe)
        function = function_output[0]
        key = function_output[1]
        url = self.base_url + f"&function={function}&symbol={symbol}&outputsize=full"
        response = requests.get(url)
        if response.status_code != 200: 
            self.logger.log(f"Error fetching stock prices for {symbol} at {timeframe}", 'CRITICAL')
            return None
        bytes_data = response.content.decode('utf-8')
        json_data = json.loads(bytes_data)
        extract_data = json_data[key]
        df = pd.DataFrame.from_dict(extract_data, orient='index')
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'date',
                           '1. open': 'open',
                            '2. high': 'high',
                            '3. low': 'low',
                            '4. close': 'close',
                            '5. volume': 'volume'
                        }, inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col])
        return df   
    
    def stock_symbol_search(self, symbol):
        url = self.base_url + f"&function=SYMBOL_SEARCH&keywords={symbol}"
        response = requests.get(url)
        if response.status_code != 200: 
            return None
        bytes_data = response.content.decode('utf-8')
        json_data = json.loads(bytes_data)
        return json_data
    
