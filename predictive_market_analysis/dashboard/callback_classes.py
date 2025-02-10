class StockDropDown():
    def __init__(self, value):
        self.options = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        self.value = [value.lower() if value in self.options else self.options[0].lower()]

class TimeFrameDropDown():
    def __init__(self, value):
        self.options = ['daily', 'intraday', 'daily_adjusted', 'weekly', 'weekly_adjusted', 'monthly', 'monthly_adjusted']
        self.value = [value if value in self.options else self.options[0]]

class MLModelSelect():
    def __init__(self, params):
        self.models = ['LSTM']
        self.value = [params['model']] if 'model' in params and params['model'] in self.models else self.models[0]
        self.value.append(params['lookback'] if 'lookback' in params and isinstance(params['lookback'], int) and params['lookback'] > 0 else 4)
        self.forecast.append(params['forecast'] if 'forecast' in params and isinstance(params['forecast'], int) and params['forecast'] > 0 else 1)
