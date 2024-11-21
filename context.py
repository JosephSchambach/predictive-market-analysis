import json
import os
import regex as re

class Context:
    def __init__(self):
        self._config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        self._get_config()
        self._get_secrets()


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
            if secret == 'alpha_vantage_url':
                self.secrets[secret] = _prepare_alpha_vantage_url(url = self.config['secrets'][secret])
            self.secrets[secret] = self.config['secrets'][secret]

    def _prepare_alpha_vantage_url(url: str = None):
        if url is None: return
        url = url+self.config['secrets']['alpha_vantage_api_key']
        return url