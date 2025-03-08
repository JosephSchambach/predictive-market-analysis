import technical_indicators as ti
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
import random
from matplotlib import pyplot as plt

start_date = datetime.strptime("2021-01-01", "%Y-%m-%d")

# getting data
data = pd.read_csv('C:/Users/JosephSchambach/source/predictive-market-analysis/data/result.csv')
data['date'] = pd.to_datetime(data['date'])

# on balance volume
data = ti.on_balance_volume(data, 'close')
# bollinger bands
data = ti.bollinger_bands(data, 20, 2, 'close')

# rsi
close = pd.DataFrame(data[['date','close']])
close.set_index('date', inplace=True)
close['rsi'] = close.ta.rsi(length=14)
close.plot()

# moving average
result = ti.moving_average(data, [50,25], 'close')
# result['spread'] = result["25_day_moving_average"] - result["50_day_moving_average"]
# result = relative_strength_index(data, 14, 'close')
# plt.plot(result['date'], close['rsi'], label='RSI')
# plt.axhline(30, linestyle='--', linewidth=1.5, color='green')
# # Overbought
# plt.axhline(70, linestyle='--', linewidth=1.5, color='red')
# plt.show()
pass