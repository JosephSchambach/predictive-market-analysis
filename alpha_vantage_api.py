import requests
import json

class AlphaVantageAPI: 
    def __init__(self, api_config): 
        self.base_url = api_config['alpha_vantage_url'] + api_config['alpha_vantage_api_key']

    def get_daily(self, symbol): 
        function = "TIME_SERIES_DAILY"
        url = self.base_url + f"&function={function}&symbol={symbol}"
        response = requests.get(url)
        if response.status_code != 200: 
            return None
        bytes_data = response.content.decode('utf-8')
        json_data = json.loads(bytes_data)
        return json_data