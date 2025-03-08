from predictive_ma.context.predictor_context import MarketPredictorContext

context = MarketPredictorContext()

class ETLClass():
    def __init__(self, symbol: str, timeframe: str):
        self.symbol = symbol
        self.timeframe = timeframe
        self.missing_table = False
        self.data = None
        self._check_database()
        self._extract_data()

    def _check_database(self):
        context.logger.log(f"Starting ETL process for {self.timeframe} {self.symbol} data")
        table_name = f'{self.symbol}_{self.timeframe}'
        response = context.database.select(table_name, ['date', 'close'])
        if response is None:
            self.missing_table = True
            context.logger.log(f"No data found for symbol: {self.symbol} and timeframe: {self.timeframe}")

    def _extract_data(self):
        self.data = context.api.execute('fetch_stock_prices', timeframe=self.timeframe, symbol=self.symbol)
        if self.data is None:
            return
        self.data = self.data[['date', 'close']]