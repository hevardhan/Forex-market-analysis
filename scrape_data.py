#Scrape data

import MetaTrader5 as mt5
import pandas as pd
import datetime
import pytz

mt5.initialize(path=r"C:\Program Files\MetaTrader 5 IC Markets (SC)\terminal64.exe")
timezone = pytz.timezone("Etc/UTC")

utc_from = datetime.datetime(2022, 1, 1, tzinfo=timezone)
utc_to = datetime.datetime(2022, 12, 31, tzinfo=timezone)
rates = mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_H4, utc_from, utc_to)

df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'],unit='s')
df.to_csv(r"C:\Users\sarav\Documents\EDA\datasets\eurusd\eurusd_test.csv")
print(df)