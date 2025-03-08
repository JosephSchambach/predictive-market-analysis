from predictive_ma.context.predictor_context import MarketPredictorContext
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt

context = MarketPredictorContext()

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
        context.logger.log(f"An error occurred on MA: {str(e)}", 'ERROR')
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
        context.logger.log(f"An error occurred on RSI: {str(e)}", 'ERROR')

def moving_average_convergence_divergence(df: pd.DataFrame, short_period: int, long_period: int, column: str):
    try:
        if isinstance(short_period, int) and isinstance(long_period, int) and column in df.columns:
            temp_df = df[['date',column]]
            temp_df.set_index('date', inplace=True)
            temp_df.ta.macd(close=column,fast=short_period, slow=long_period, append=True)
            temp_df.reset_index(inplace=True)
            return df.merge(temp_df[['date','MACD_12_26_9','MACDh_12_26_9','MACDs_12_26_9']], on='date', how='left')
    except Exception as e:
        context.logger.log(f"An error occurred on MACD: {str(e)}", 'ERROR')

def bollinger_bands(df: pd.DataFrame, length: int, std: int, column: str):
    try:
        if isinstance(length, int) and isinstance(std, int) and column in df.columns:
            temp_df = df[['date',column]]
            temp_df.set_index('date', inplace=True)
            temp_df.ta.bbands(length=length, std=std, append=True)
            temp_df.reset_index(inplace=True)
            columns_to_merge = ['date',f"BBL_{length}_{std}.0",f"BBM_{length}_{std}.0",f"BBU_{length}_{std}.0",f"BBB_{length}_{std}.0",f"BBP_{length}_{std}.0"]
            return df.merge(temp_df[columns_to_merge], on='date', how='left')
    except Exception as e:
        context.logger.log(f"An error occurred on Bollinger Bands: {str(e)}", 'ERROR')

def on_balance_volume(df: pd.DataFrame, column: str): 
    try: 
        if column in df.columns:
            temp_df = df[['date',column, 'volume']]
            temp_df.set_index('date', inplace=True)
            temp_df.ta.obv(append=True)
            temp_df.reset_index(inplace=True)
            return df.merge(temp_df[['date','OBV']], on='date', how='left')
    except Exception as e:
        context.logger.log(f"An error occurred on OBV: {str(e)}", 'ERROR')
