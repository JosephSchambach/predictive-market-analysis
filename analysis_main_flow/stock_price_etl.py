from predictive_ma.context.predictor_context import MarketPredictorContext
from predictive_ma.database.etl_class import ETLClass

context = MarketPredictorContext()

class StockPriceETL():
    def __init__(self):
        self.symbols = context.stock_symbols
        self.timeframes = context.timeframes

    def perform_etl(self):
        for symbol in self.symbols:
            for timeframe in self.timeframes:
                context.database.etl(ETLClass(symbol=symbol.lower(), timeframe=timeframe))
        context.logger.log('ETL process completed')
        
if __name__ == '__main__':
    stock = StockPriceETL()
    stock.perform_etl()