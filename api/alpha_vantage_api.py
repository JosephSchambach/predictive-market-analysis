import requests
import json
import pandas as pd

class AlphaVantageAPI: 
    def __init__(self, api_config): 
        self.base_url = api_config['alpha_vantage_url'] + api_config['alpha_vantage_api_key']

    def fetch_stock_prices(self, function, symbol): 
        function = "TIME_SERIES_DAILY"
        url = self.base_url + f"&function={function}&symbol={symbol}"
        response = requests.get(url)
        if response.status_code != 200: 
            return None
        bytes_data = response.content.decode('utf-8')
        json_data = json.loads(bytes_data)
        extract_data = json_data['Time Series (Daily)']
        df = pd.DataFrame.from_dict(extract_data, orient='index')
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'date',
                           '1. open': 'open',
                            '2. high': 'high',
                            '3. low': 'low',
                            '4. close': 'close',
                            '5. volume': 'volume'
                        }, inplace=True)
        return df   
    
    def stock_symbol_search(self, symbol):
        url = self.base_url + f"&function=SYMBOL_SEARCH&keywords={symbol}"
        response = requests.get(url)
        if response.status_code != 200: 
            return None
        bytes_data = response.content.decode('utf-8')
        json_data = json.loads(bytes_data)
        return json_data
    
