from technical_indicators import moving_average, relative_strength_index, moving_average_convergence_divergence
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
import random
from matplotlib import pyplot as plt

start_date = datetime.strptime("2021-01-01", "%Y-%m-%d")

data = pd.read_csv('C:/Users/JosephSchambach/source/predictive-market-analysis/data/result.csv')
data = moving_average_convergence_divergence(data, 12, 26, 'close')
# data['date'] = pd.to_datetime(data['date'])
# close = pd.DataFrame(data[['date','close']])
# close.set_index('date', inplace=True)
# close['rsi'] = close.ta.rsi(length=14)
# close.plot()
# result = moving_average(data, [50,25], 'close')
# result['spread'] = result["25_day_moving_average"] - result["50_day_moving_average"]
# result = relative_strength_index(data, 14, 'close')
# plt.plot(result['date'], close['rsi'], label='RSI')
# plt.axhline(30, linestyle='--', linewidth=1.5, color='green')
# # Overbought
# plt.axhline(70, linestyle='--', linewidth=1.5, color='red')
# plt.show()
pass