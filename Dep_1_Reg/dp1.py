import pickle
import MetaTrader5 as mt5
import pandas as pd
with open('Dep_1_Reg\lin_reg.pkl', 'rb') as file:
    model = pickle.load(file)

mt5.initialize()
#-------------------------------------------------------------------------------------------------------------------------------

#INPUTS
SYMBOL       = input("Enter the Symbol")
TIMEFRAME    = mt5.TIMEFRAME_H4
VOLUME       = 1.0
DEVIATION    = 10
point        = mt5.symbol_info(SYMBOL).point
MAX_DIST_SL  = 50  * point
TRAIL_AMOUNT = 40  * point 
DEFAULT_SL   = 40  * point
TP           = 100 * point

#--------------------------------------------------------------------------------------------------------------------------------

def market_order(symbol, volume, order_type, **kwargs):
    tick = mt5.symbol_info_tick(symbol)
    point = mt5.symbol_info(symbol).point
    order_dict = {'buy': 0, 'sell': 1}
    price_dict = {'buy': tick.ask, 'sell': tick.bid}
    if order_type == 'buy':
        sl = price_dict[order_type] - 50 * point
        tp = price_dict[order_type] + 100 * point
    elif order_type == 'sell':
        sl = price_dict[order_type] + 50 * point
        tp = price_dict[order_type] - 100 * point
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_dict[order_type],
        "price": price_dict[order_type],
        "deviation": DEVIATION,
        "sl" : sl,
        "tp" : tp,
        "magic": 100,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    order_result = mt5.order_send(request)
    print(order_result)

    return order_result

rates = mt5.copy_rates_from_pos(SYMBOL,TIMEFRAME,0,1)
rates_df = pd.DataFrame(rates)
print(rates_df)