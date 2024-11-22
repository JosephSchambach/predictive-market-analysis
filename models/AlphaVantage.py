def get_function(timeframe: str):
    if len(timeframe) == 0: return None
    if len(timeframe.split())> 1: timeframe = '_'.join(timeframe.split())
    timeframe = timeframe.lower()
    func_dict = {
        'daily': 'TIME_SERIES_DAILY',
        'intraday': 'TIME_SERIES_INTRADAY',
        'daily_adjusted': 'TIME_SERIES_DAILY_ADJUSTED',
        'weekly': 'TIME_SERIES_WEEKLY', 
        'weekly_adjusted': 'TIME_SERIES_WEEKLY_ADJUSTED',
        'monthly': 'TIME_SERIES_MONTHLY',
        'monthly_adjusted': 'TIME_SERIES_MONTHLY_ADJUSTED'
    }
    return func_dict[timeframe]