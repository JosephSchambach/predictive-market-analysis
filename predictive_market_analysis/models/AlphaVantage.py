from predictive_market_analysis.context.predictor_context import MarketPredictorContext

context = MarketPredictorContext()

def get_function(timeframe: str, interval=None):
    try:
        if timeframe not in ['daily','intraday','daily_adjusted','weekly','weekly_adjusted','monthly','monthly_adjusted']:
            context.logger.log(f"Invalid timeframe: {timeframe}", 'ERROR')
            raise ValueError(f"Invalid timeframe: {timeframe}")
        if len(timeframe.split())> 1: timeframe = '_'.join(timeframe.split())
        timeframe = timeframe.lower()
        if timeframe == 'intraday' and interval is None: interval = '5min'
        elif timeframe == 'intraday' and interval is not None: interval = interval.lower()
        func_dict = {
            'daily': ['TIME_SERIES_DAILY','Time Series (Daily)'],
            'intraday': ['TIME_SERIES_INTRADAY',f"Time Series ({interval})"],
            'daily_adjusted': ['TIME_SERIES_DAILY_ADJUSTED','Time Series (Daily)'],
            'weekly': ['TIME_SERIES_WEEKLY','Weekly Time Series'], 
            'weekly_adjusted': ['TIME_SERIES_WEEKLY_ADJUSTED','Weekly Adjusted Time Series'],
            'monthly': ['TIME_SERIES_MONTHLY','Monthly Time Series'],
            'monthly_adjusted': ['TIME_SERIES_MONTHLY_ADJUSTED','Monthly Adjusted Time Series']
        }
        return func_dict[timeframe]
    except Exception as e:
        context.logger.log(f"An error occurred in AlphaVantage get_function: {str(e)}", 'ERROR')