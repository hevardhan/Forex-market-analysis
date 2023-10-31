import MetaTrader5 as mt5
import pandas as pd
import pickle
import numpy as np
import tkinter as t
from tkinter import ttk
from tkinter import messagebox
mt5.initialize(path=r"C:\Program Files\MetaTrader 5 IC Markets (SC)\terminal64.exe")
def start_trading():
    SYMBOL = n.get()
    VOLUME = float(vol_entry.get())
    DEVIATION = int(dev_entry.get())
    def market_order(symbol, volume, order_type, **kwargs):
        tick = mt5.symbol_info_tick(symbol)
        point = mt5.symbol_info(symbol).point
        order_dict = {'buy': 0, 'sell': 1}
        price_dict = {'buy': tick.ask, 'sell': tick.bid}
        # if order_type == 'buy':
        #     sl = price_dict[order_type] - 50 * point
        #     tp = price_dict[order_type] + 100 * point
        # elif order_type == 'sell':
        #     sl = price_dict[order_type] + 50 * point
        #     tp = price_dict[order_type] - 100 * point
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_dict[order_type],
            "price": price_dict[order_type],
            "deviation": DEVIATION,
            # "sl" : sl,
            # "tp" : tp,
            "magic": 100,
            "comment": "python market order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        order_result = mt5.order_send(request)
        print(order_result)

        return order_result


    TIMEFRAME = mt5.TIMEFRAME_H4
    rates = mt5.copy_rates_from_pos(SYMBOL,TIMEFRAME,0,20)
    df = pd.DataFrame(rates)
    print(df)
    df['SMA10'] = df['close'].rolling(10).mean()
    df['SMA20'] = df['close'].rolling(20).mean()
    def signal(raw):
        
        if raw['SMA10'] > raw['SMA20']:
            return 1
        elif raw['SMA10']  < raw['SMA20']:
            return 0
        else :
            return np.NaN

    df['Signal'] = df.apply(signal,axis=1)
    # df['time'] = pd.to_datetime(df['time'],unit='s')
    # print(type(df['time'][0]))
    # df.rename(columns={'time':'timestamp_unix'},inplace=True)
    df['timestamp_unix'] = df['time'].astype(np.int64) / 10**9 
    df.dropna(inplace=True)
    if mo_ch.get() == 'Linear Regression':
        model = pickle.load(open(r"D:\SY - Class\Forex-market-analysis\Dep_1_Reg\lin_reg.pkl","rb"))    
        y = model.predict(df[['timestamp_unix','open','high','low','close','SMA10','SMA20','Signal']])
        cat = [1 if y[0] >= 0.5 else 0]
    else : 
        model = pickle.load(open(r"rfc.pkl","rb"))
        y = model.predict(df[['timestamp_unix','open','high','low','close','SMA10','Signal','SMA20']])
        cat = y
    # signal = [1 if p[0] >= 0.5 else 0 for p in y]
    # print(y)
    # print(signal)
    signal = df['Signal'].to_list()
    print(cat)
    # # print(signal)
    if cat[0] == 1:
        if signal[0] == 1:
            market_order(SYMBOL,VOLUME,"buy")
            messagebox.showinfo("","Buy Order Placed Successfully")
        elif signal[0] == 0:
            market_order(SYMBOL,VOLUME,'sell')
            messagebox.showinfo("","Sell Order Placed Successfully")
        else :
            messagebox.showinfo("","Order Not Placed - Non-Profitable Signal")

main = t.Tk()
main.state('zoomed')
main.resizable(0,0)

label = t.Label(main,text='Algorithmic Trading',font=('Poppins',30))
txt_3 =     t.Label(main,text="Choose the Model : ",font=('Poppins Light',15))
mo_ch = t.StringVar()
mo_choice = ttk.Combobox(main,textvariable=mo_ch)
mo_choice['values'] = ('Linear Regression','Random Forest Classifier')
n = t.StringVar() 
choice = ttk.Combobox(main,textvariable=n)
choice['values'] = ('EURUSD','AUDUSD','USDCHF')

txt_1 =     t.Label(main,text="Choose the Symbol : ",font=('Poppins Light',15))
dev_label = t.Label(main,text='Enter the Deviation : ',font=('Poppins Light',15))
dev_entry = t.Entry(main,font=('Poppins Light',12))

vol_label = t.Label(main,text="Enter the Volume    : ",font=('Poppins Light',15))
vol_entry = t.Entry(main,font=('Poppins Light',12))

start_trade_btn = t.Button(main,text="Predict and Place Order",font=('Poppins Light',12),command=start_trading)
label.place(x=200,y=100)
txt_1.place(x=200,y=200)
choice.place(x=420,y=210)

txt_3.place(x=200,y=550)
mo_choice.place(x=420,y=560)

dev_label.place(x=200,y=300)
dev_entry.place(x=420,y=305)

vol_label.place(x=200,y=400)
vol_entry.place(x=420,y=405)

start_trade_btn.place(x=200,y=650)
main.mainloop()

