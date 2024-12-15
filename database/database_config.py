from api.supabase_api import SupabaseAPI
import pandas as pd

class Database():
    def __init__(self,database_config):
        if 'supabase' in database_config:
            self._supabase = SupabaseAPI(database_config=database_config['supabase'])
        else:
            raise AttributeError("Database configuration not found.")

    def query(self, table_name):
        if self._supabase:
            return self._supabase.fetch_supabase_data(table_name)
        return None
