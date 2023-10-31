import streamlit as st
import numpy as np
import pandas as pd
import requests
import datetime
import MetaTrader5 as mt5
import pickle
import time
mt5.initialize()

DEVIATION = 10

def market_order(symbol, volume, order_type, **kwargs):
    tick = mt5.symbol_info_tick(symbol)
    order_dict = {'buy': 0, 'sell': 1}
    price_dict = {'buy': tick.ask, 'sell': tick.bid}
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_dict[order_type],
        "price": price_dict[order_type],
        "deviation": DEVIATION,
        "magic": 100,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    order_result = mt5.order_send(request)
    print(order_result)

    return order_result

#---------------------------------------------------------------------------------------------------------------------------------

def close_order(ticket,symbol):
    positions = mt5.positions_get()

    for pos in positions :
        tick = mt5.symbol_info_tick(pos.symbol)
        type_dict = {0: 1, 1: 0}  # 0 represents buy, 1 represents sell - inverting order_type to close the position
        price_dict = {0: tick.ask, 1: tick.bid}
        
        if pos.ticket==ticket and pos.symbol == symbol:
            request = {
                    "action":mt5.TRADE_ACTION_DEAL,
                    "position":pos.ticket,
                    "symbol":pos.symbol,
                    "volume":pos.volume,
                    "type":type_dict[pos.type],
                    "price":price_dict[pos.type],
                    "deviation": DEVIATION,
                    "magic":100,
                    "comment":"python close order",
                    "type_time":mt5.ORDER_TIME_GTC,
                    "type_filling":mt5.ORDER_FILLING_IOC,
            }           
            order_result = mt5.order_send(request)
            print(order_result)
            
            return order_result
        
    return "Ticket doesn't Exist"  

def get_exposure(symbol):
    positions = mt5.positions_get(symbol=symbol)
    if positions:
        pos_df = pd.DataFrame(positions,columns=positions[0]._asdict().keys())
        exposure = pos_df['volume'].sum()
        
        return exposure


def trade(symbol, volume):
    SYMBOL = symbol
    VOLUME = volume
    TIMEFRAME = mt5.TIMEFRAME_H4
    while True:
        exposure = get_exposure(SYMBOL)

        rates = mt5.copy_rates_from_pos(SYMBOL,TIMEFRAME,0,20)
        df = pd.DataFrame(rates)
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
        model = pickle.load(open(r"D:\SY - Class\Forex-market-analysis\rfc.pkl","rb"))
        y = model.predict(df[['timestamp_unix','open','high','low','close','SMA10','Signal','SMA20']])
        pred_test = y
        direction = None
        if pred_test[0] == 1 :
            direction = 'buy'
        elif pred_test[0] == 0 :
            direction = 'sell'
            
        # trading logic
        if direction == 'buy':
            # if we have a BUY signal, close all short positions
            for pos in mt5.positions_get():
                if pos.type == 1 and pos.symbol == SYMBOL:  # pos.type == 1 represent a sell order
                    close_order(pos.ticket,SYMBOL)
            flag = True
            for pos in mt5.positions_get():
                if pos.symbol != SYMBOL:
                    flag = False
                    break
            # if there are no open positions, open a new long position
            if (flag == False and exposure == None) or (mt5.positions_total() == 0):
                market_order(SYMBOL, VOLUME, direction)

        elif direction == 'sell':
            # if we have a SELL signal, close all short positions
            for pos in mt5.positions_get():
                if pos.type == 0 and pos.symbol == SYMBOL:  # pos.type == 0 represent a buy order
                    close_order(pos.ticket,SYMBOL)

            # if there are no open positions, open a new short position
            flag = True
            for pos in mt5.positions_get():
                if pos.symbol != SYMBOL:
                    flag = False
                    break
            if (flag == False and exposure == None) or (mt5.positions_total() == 0):
                market_order(SYMBOL, VOLUME, direction)
        
        st.write("Time                  :",datetime.datetime.now())
        st.write("Exposure              :",exposure)
        st.write("SIGNAL                :",direction)
        st.write("SYMBOL                :",SYMBOL)
        st.write("TIMEFRAME             :",str(TIMEFRAME))
        st.write("----------------------\n")
        
        if len(mt5.positions_get()) >= 1:
            time.sleep(10)
        elif direction == None:
            time.sleep(1)
            continue
        else:
            time.sleep(1)
            continue    

def main():
    st.title("Trade Input App")
    
    # Input fields
    SYMBOL = st.text_input("Enter Symbol:", "")
    VOLUME = st.number_input("Enter Volume:", min_value=0)
    
    # Start Trading button
    if st.button("Start Trading"):
            trade(SYMBOL, VOLUME)

if __name__ == "__main__":
    main()
