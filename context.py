from api.api_config import API
from logging_context import Logger
from database.database_config import Database
import json
import os

class MarketPredictorContext:
    def __init__(self):
        self._config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        self._get_logger()
        self._get_config()
        self._get_secrets()
        self._get_api()
        self._get_database()

    def _get_logger(self): 
        self.logger = Logger()
        
    def _get_config(self):
        if self._config_path is None: return
        with open(self._config_path, 'r') as config_file:
            config = json.load(config_file)
        self.config = config
        return self.config
    
    def _get_secrets(self):
        self.secrets = {}
        if 'secrets' not in self.config: return
        for secret in self.config['secrets']:
            for var in self.config['secrets'][secret]: 
                self.secrets[secret + "_" + var] = self.config['secrets'][secret][var]

    def _get_api(self):
        api_config = self.secrets
        config = self.config['secrets']
        self.api = API(api_config=api_config, config=config, logger=self.logger)

    def _get_database(self):
        if 'database' not in self.config['secrets']: return
        self.database = Database(database_config=self.config['secrets']['database'], logger=self.logger)
