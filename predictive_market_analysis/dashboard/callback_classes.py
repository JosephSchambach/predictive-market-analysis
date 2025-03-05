class StockDropDown():
    def __init__(self, value):
        self.options = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        self.value = [value.lower() if value in self.options else self.options[0].lower()]

class TimeFrameDropDown():
    def __init__(self, value):
        self.options = ['daily', 'weekly', 'monthly']
        self.value = [value if value in self.options else self.options[0]]

class MLModelSelect():
    def __init__(self, params):
        self.no_model = False
        if params == {}: self.no_model = True
        self.models = ['Long-Short-Term-Memory']
        self.model = [params['model']] if 'model' in params and params['model'] in self.models else self.models[0]
        self.lookback = int(params['lookback']) if 'lookback' in params and isinstance(params['lookback'], int) and params['lookback'] > 0 else 4
        self.forecast = int(params['forecast']) if 'forecast' in params and isinstance(params['forecast'], int) and params['forecast'] > 0 else 1
