from supabase import create_client, Client
import hashlib
import pandas as pd

class Database():
    def __init__(self,database_config, logger):
        self._database_url = database_config['supabase']['api_url']
        self._database_key = database_config['supabase']['api_key']
        self._etl_config = database_config['etl'] if 'etl' in database_config else None
        self._supabase: Client = create_client(self._database_url, self._database_key)
        self.logger = logger
    
    def select(self, table: str, columns: str | list):
        if self._supabase: 
            try:
                if table == '': 
                    raise ValueError("Table name cannot be empty.")
                processed_columns = self._process_columns(columns)
                self.logger.log(f"Selecting columns: {processed_columns}")
                response = self._supabase.table(table).select(processed_columns).gt("date", "2023-12-31").order("date", desc=False).execute()
                if response.data is None:
                    return
                df = pd.DataFrame(response.data)
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                if 'close' in df.columns:
                    df['close'] = df['close'].astype(float)
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
    
    def create(self, table: str, columns_datatypes: dict):
        if self._supabase:
            try:
                if table == '' or columns_datatypes == {}:
                    raise ValueError("Table name and columns cannot be empty.")
                self.logger.log(f"Creating table: {table}")
                str_columns = ','.join([f"{col} {datatype}" for col, datatype in columns_datatypes.items()])
                response = self._supabase.rpc('create_dynamic_table', {'table_name':table, 'columns':str_columns}).execute()
                return response
            except Exception as e:
                self.logger.log(f"Database action create failed with error: {str(e)}", 'CRITICAL')
        return None

    def etl(self, symbol: str, timeframe: str):
        if self._etl_config is None:
            self.logger.log('ETL config is not set', 'ERROR')
            return
        try:
            self.logger.log(f"Running ETL for symbol: {symbol} and timeframe: {timeframe}")
            response = self.select(f"{symbol}_{timeframe}", ['date', 'close'])
            if response.empty:
                self.logger.log(f"No data found for symbol: {symbol} and timeframe: {timeframe}")
                
                columns = {
                    'id': 'text',
                    'date': 'date', 
                    'close': 'text'
                }
                create_res = self.create(f"{symbol}_{timeframe}", columns)
                if create_res is None:
                    self.logger.log(f"Table {symbol}_{timeframe} not created successfully")
                    return
                else:
                    self.logger.log(f"Table {symbol}_{timeframe} created successfully")
                    # need to figure out a way to call the api for data. Maybe this needs to be a paramater. TODO
            return response
        except Exception as e:
            self.logger.log(f"Database action etl failed with error: {str(e)}", 'CRITICAL')
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

    
