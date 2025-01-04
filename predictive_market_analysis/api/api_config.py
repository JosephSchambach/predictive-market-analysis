from predictive_market_analysis.api.alpha_vantage_api import AlphaVantageAPI
from predictive_market_analysis.api.dashboard_api import DashboardAPI
import pandas as pd
import requests 
import os

class API():
    def __init__(self, api_config, config, logger): 
        self.logger = logger
        if 'alpha_vantage' in config:
            self._alpha_vantage = AlphaVantageAPI(api_config=api_config, logger=logger)
        if 'dashboard' in config:
            self._dashboard = DashboardAPI(logger=logger)
        if 'file' in config: 
            self._files = config['file']['path']

    def execute(self, method_name, **kwargs):
        self.logger.log(f"Executing method: {method_name}")
        try:
            if self._alpha_vantage and hasattr(self._alpha_vantage, method_name):
                method = getattr(self._alpha_vantage, method_name)
                return method(**kwargs)
            if self._dashboard and hasattr(self._dashboard, method_name):
                method = getattr(self._dashboard, method_name)
                return method(**kwargs)
            if self._files:
                path_to_file = self._files + kwargs['file']
                if method_name == 'file_read': 
                    if os.path.exists(path_to_file):
                        data = pd.read_csv(path_to_file)
                        return data
            self.logger.log(f"The method {method_name} does not exist on the API instance.")
            raise AttributeError(f"The method {method_name} does not exist on the API instance.")
        except Exception as e:
            self.logger.log(f"Error executing method: {method_name} with error {str(e)}", 'CRITICAL')
            return
    
    def visualize(self, method_name, **kwargs):
        self.logger.log(f'Visualizing data using method: {method_name}')
        if self._alpha_vantage and hasattr(self._alpha_vantage, method_name):
            method = getattr(self._alpha_vantage, method_name)
            return method(**kwargs)
        self.logger.log(f"The method {method_name} does not exist on the API instance.")
        raise AttributeError(f"The method {method_name} does not exist on the API instance.")