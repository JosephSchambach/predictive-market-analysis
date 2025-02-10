from predictive_market_analysis.context.predictor_context import MarketPredictorContext

context = MarketPredictorContext()

class ETLClass():
    def __init__(self, symbol: str, timeframe: str):
        self.symbol = symbol
        self.timeframe = timeframe
        self.missing_table = False
        self.data = None
        self._check_database()

    def _check_database(self):
        table_name = f'{self.symbol}_{self.timeframe}'
        response = context.database.select(table_name, ['date', 'close'])
        if response is None:
            self.missing_table = True
            self._extract_data()
        elif not response.empty:
            self.data = response

    def _extract_data(self):
        if self.missing_table:
            self.data = context.api.execute('fetch_stock_prices', timeframe=self.timeframe, symbol=self.symbol)
            self.data = self.data[['date', 'close']]