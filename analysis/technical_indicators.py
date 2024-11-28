import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt

def moving_average(df: pd.DataFrame, period: list, column: str):
    try:
        if isinstance(period, int):
            period = [period]
        if not isinstance(period, list): 
            raise ValueError("Period must be a list")
        if column not in df.columns: 
            raise ValueError("Column does not exist in the DataFrame")
        for p in period: 
            column_name = f"{p}_day_moving_average"
            df[column_name] = round(df[column].rolling(window=p).mean(),2)
    except Exception as e:
        print(f"An error occurred: {e}")
    return df

def relative_strength_index(df: pd.DataFrame, period: int, column: str): 
    try: 
        if isinstance(period, int) and column in df.columns:
            temp_df = df[['date',column]]
            temp_df.set_index('date', inplace=True)
            temp_df['rsi'] = temp_df.ta.rsi(length=period)
            temp_df.reset_index(inplace=True)
            return df.merge(temp_df[['date','rsi']], on='date', how='left')
    except Exception as e: 
        print(f"An error occurred: {e}")

def moving_average_convergence_divergence(df: pd.DataFrame, short_period: int, long_period: int, column: str):
    try:
        if isinstance(short_period, int) and isinstance(long_period, int) and column in df.columns:
            temp_df = df[['date',column]]
            temp_df.set_index('date', inplace=True)
            temp_df.ta.macd(close=column,fast=short_period, slow=long_period, append=True)
            temp_df.reset_index(inplace=True)
            return df.merge(temp_df[['date','MACD_12_26_9','MACDh_12_26_9','MACDs_12_26_9']], on='date', how='left')
    except Exception as e:
        print(f"An error occurred: {e}")


