from alpha_vantage_api import AlphaVantageAPI
import requests

class API():
    def __init__(self, api_config, config): 
        if 'alpha_vantage' in config:
            self._alpha_vantage = AlphaVantageAPI(api_config=api_config)

