from alpha_vantage_api import AlphaVantageAPI
import requests

class API():
    def __init__(self, api_config, config): 
        if 'alpha_vantage' in config:
            self._alpha_vantage = AlphaVantageAPI(api_config=api_config)

    def execute(self, method_name, **kwargs):
        if self._alpha_vantage and hasattr(self._alpha_vantage, method_name):
            method = getattr(self._alpha_vantage, method_name)
            return method(**kwargs)
        raise AttributeError(f"The method {method_name} does not exist on the API instance.")