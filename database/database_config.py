from supabase import create_client, Client
import hashlib
import pandas as pd

class Database():
    def __init__(self,database_config, logger):
        self._database_url = database_config['supabase']['api_url']
        self._database_key = database_config['supabase']['api_key']
        self._supabase: Client = create_client(self._database_url, self._database_key)
        self.logger = logger
    
    def select(self, table: str, columns: str | list):
        if self._supabase: 
            try:
                if table == '': 
                    raise ValueError("Table name cannot be empty.")
                processed_columns = self._process_columns(columns)
                self.logger.log(f"Selecting columns: {processed_columns}")
                response = self._supabase.table(table).select(processed_columns).execute()
                if response.data is None:
                    return
                df = pd.DataFrame(response.data)
                return df
            except Exception as e:
                self.logger.log(f"Database select action select failed with error: {str(e)}",'CRITICAL')

    def insert(self, table: str, data: pd.DataFrame):
        if self._supabase:
            try:
                if table == '':
                    raise ValueError("Table name cannot be empty.")
                if data.empty:
                    return
                data_with_id = self._handle_id_column(data)
                rows = self._row_create(data_with_id)
                self.logger.log(f"Inserting data into table: {table}")
                response = self._supabase.table(table).insert(rows).execute()
                return response
            except Exception as e:
                self.logger.log(f"Database action insert failed with error: {str(e)}", 'CRITICAL')

    def upsert(self, table: str, data: pd.DataFrame):
        if self._supabase:
            try: 
                if table == '':
                    raise ValueError("Table name cannot be empty.")
                if data.empty:
                    return
                data_with_id = self._handle_id_column(data)
                rows = self._row_create(data_with_id)
                self.logger.log(f"Upserting data into table: {table}")
                response = self._supabase.table(table).upsert(rows).execute()
                return response
            except Exception as e:
                self.logger.log(f"Database action upsert failed with error: {str(e)}",'CRITICAL')
        return None
    
    def _process_columns(self, columns: str | list):
        if isinstance(columns, list) and not columns:
            raise ValueError("Column list cannot be empty.")
        return ','.join(map(str, columns)) if isinstance(columns, list) else str(columns)
    
    def _handle_id_column(self, df: pd.DataFrame):
        data = df.dropna()
        def _generate_hash(id_column): 
            is_string = isinstance(id_column, str)
            if is_string:
                return hashlib.sha256(id_column.encode('utf-8')).hexdigest()
            return hashlib.sha256(str(id_column).encode('utf-8')).hexdigest()
        if data.empty: 
            return data
        if 'id' not in data.columns:
            data['id'] = ''
            for col in data.columns:
                if col != 'id':
                    data['id'] += data[col].astype(str)
            data['id'] = data['id'].apply(_generate_hash)
            return data
        else:
            return data
            
    def _row_create(self, data: pd.DataFrame):
        try: 
            if data.empty:
                return []
            rows = data.to_dict(orient='records')
            return rows
        except Exception as e: 
            self.logger.log(f"Database action row_create failed with error: {str(e)}", 'ERROR')
