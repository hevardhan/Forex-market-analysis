import yfinance as yf
import numpy as np

# Define the currency pair symbol
currency_pair = 'EURUSD=X'

# Download the recent 10 values for a 15-minute chart
data = yf.Ticker(currency_pair)
recent_data = data.history(period="1d", interval="15m", actions=False)

# Print the recent 10 values
df = recent_data.tail(20)
df.reset_index(inplace=True)
df['timestamp_unix'] = (df['Datetime'].astype(np.int64) / 10**9).astype(int)
df['SMA10'] = df['Close'].rolling(10).mean()
df['SMA20'] = df['Close'].rolling(20).mean()
def signal(raw):
    
    if raw['SMA10'] > raw['SMA20']:
        return 1
    elif raw['SMA10']  < raw['SMA20']:
        return 0
    else :
        return None

df['Signal'] = df.apply(signal,axis=1)
signal = df['Signal'].to_list()
df = df.tail(1)
print(df)
