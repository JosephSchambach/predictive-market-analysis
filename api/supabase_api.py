from supabase import create_client, Client
import pandas as pd

class SupabaseAPI: 
    def __init__(self, database_config): 
        self._database_url = database_config['api_url']
        self._database_key = database_config['api_key']
        self.client: Client = create_client(self._database_url, self._database_key)

    def fetch_supabase_data(self, table_name): 
        response = self.client.table(table_name).select('*').execute()
        if response.data is None:
            return None
        df = pd.DataFrame(response.data)
        return df