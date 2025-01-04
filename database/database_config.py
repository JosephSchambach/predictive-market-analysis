from supabase import create_client, Client
import hashlib
import pandas as pd

class Database():
    def __init__(self,database_config):
        if 'supabase' in database_config:
            self._database_url = database_config['supabase']['api_url']
            self._database_key = database_config['supabase']['api_key']
            self._supabase: Client = create_client(self._database_url, self._database_key)
        else:
            raise AttributeError("Database configuration not found.")
    
    def select(self, table: str, columns: str | list):
        if self._supabase: 
            processed_columns = self._process_columns(columns)
            response = self._supabase.table(table).select(processed_columns).execute()
            if response.data is None:
                return None
            df = pd.DataFrame(response.data)
            return df
        return None

    def insert(self, table: str, data: pd.DataFrame):
        if self._supabase:
            try:
                data_with_id = self._handle_id_column(data)
                rows = self._row_create(data_with_id)
                response = self._supabase.table(table).insert(rows).execute()
                return response
            except Exception as e:
                return f"Database action insert failed with error: {str(e)}"

    def upsert(self, table: str, data: pd.DataFrame):
        if self._supabase:
            try: 
                data_with_id = self._handle_id_column(data)
                rows = self._row_create(data_with_id)
                response = self._supabase.table(table).upsert(rows).execute()
                return response
            except Exception as e:
                return f"Database action upsert failed with error: {str(e)}"
        return None
    
    def _process_columns(self, columns: str | list):
        if isinstance(columns, list) and len(columns) == 0:
            return str(columns[0])
        elif isinstance(columns, list):
            columns = ','.join(str(col) for col in columns)
        return columns
    
    def _handle_id_column(self, data: pd.DataFrame):
        def _generate_hash(id_column): 
            return hashlib.sha256(id_column.encode('utf-8')).hexdigest()
        if 'id' not in data.columns:
            data['id'] = ''
            for col in data.columns:
                data['id'] += data[col].astype(str)
            data['id'] = data['id'].apply(_generate_hash)
            return data
        else:
            return data
            

    def _row_create(self, data: pd.DataFrame):
        rows = []
        for index, row in data.iterrows():
            rows.append(row.to_dict())
        return rows
