from predictive_ma.context.predictor_context import MarketPredictorContext
import pandas as pd

context = MarketPredictorContext()

def handler():
    context.dashboard.layout('Stock Price Dashboard', subtitle='Interactive Dashboard: Change Stock Symbol and Timeframe and select Machine Learning Forecast parameters if desired')
    context.dashboard.run()


if __name__ == '__main__':
    handler()