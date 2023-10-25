import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
import pickle5 as pickle
import numpy as np
import pytz
st.title("Forex-Market-Analysis")
choice = st.sidebar.selectbox("Select the Symbol",("EURUSD"," "))


type_choice = st.sidebar.selectbox("Choose the Operation",("Visualization","Prediction"))
if choice == "EURUSD":
    if type_choice == 'Visualization':
        graph_choice = st.selectbox("Choose the Type of graph",("Candle Stick","Box plot","Histogram","Line plot"))
        # tf_choice = st.selectbox("Select the Timeframe",("5 Min","15 Min","30 Min","1 Hr","4 Hr","12 hr","Daily","Weekly","Monthly"))
        # if tf_choice == "4 Hr":
        df = pd.read_csv(r"C:\Users\sarav\Documents\EDA\datasets\eurusd\eurusd_h4.csv")
        del df['Unnamed: 0']
        slider = st.number_input("Enter the Number of Rows to Display",value=10)       
        st.dataframe(df.head(slider))
        ddf = df.head(slider)
        if st.button("Show graph"):
            if graph_choice == 'Candle Stick':
                fig = go.Figure(data=[go.Candlestick(x=ddf['time'],
                    open=ddf['open'],
                    high=ddf['high'],
                    low=ddf['low'],
                    close=ddf['close'])])

                st.plotly_chart(fig)
            elif graph_choice == 'Box plot':
                fig = px.box(ddf, y=["open", "high", "low", "close"], boxmode="overlay")  # Replace "Category" and "Value" with your actual column name
                fig.update_layout(
                    title="Box Plot of Open, High, Low, and Close Values",
                    yaxis_title="Price",
                )
                # Show the plot
                st.plotly_chart(fig)
            elif graph_choice == 'Histogram':
                fig = px.histogram(ddf, x=["open", "high", "low", "close"])

                # Customize the plot
                fig.update_layout(
                    title="Histogram of Open, High, Low, and Close Values",
                    xaxis_title="Price",
                    yaxis_title="Count",
                )
                st.plotly_chart(fig)
            elif graph_choice == 'Line plot':
                ddf['SMA10'] = ddf['close'].rolling(10).mean()
                ddf['SMA20'] = ddf['close'].rolling(20).mean()
                fig = px.line(ddf, x="time", y=["close", "SMA10", "SMA20"])

                # Customize the plot (optional)
                fig.update_layout(
                    xaxis_title="Time",
                    yaxis_title="Value",
                    title="Line Plot of Close, SMA10, and SMA20",
                )
                st.plotly_chart(fig)
                

    else :
        model_choose = st.selectbox("Select the Model",("Random Forest Classification","Linear Regression")) 
        open_   = st.number_input("Enter Open Price")
        high   = st.number_input("Enter High Price")
        low    = st.number_input("Enter Low Price")
        close  = st.number_input("Enter Close Price")
        SMA10  = st.number_input("Enter SMA 10 Value")
        SMA20  = st.number_input("Enter SMA 20 Value")
        # Create a DataFrame
        data = {
            "open": [open_],
            "high": [high],
            "low": [low],
            "close": [close],
            "SMA10": [SMA10],
            "SMA20": [SMA20],
        }
        df = pd.DataFrame(data)
        timezone = pytz.timezone("Etc/UTC")
        df['time'] = datetime.datetime.now()
        df['timestamp_unix'] = (df['time'].astype(np.int64) / 10**9).astype(int)
        def signal(raw):
            
            if raw['SMA10'] > raw['SMA20']:
                return 1
            elif raw['SMA10']  < raw['SMA20']:
                return 0
            else :
                return None

        df['Signal'] = df.apply(signal,axis=1)
        signal = df['Signal'].to_list()
        
        if st.button("show"):
            if model_choose == 'Linear Regression':
                # Load the pickled model
                with open(r"Dep_1_Reg\lin_reg.pkl", "rb") as model_file:
                    model = pickle.load(model_file)
                if signal[0] != None:
                    y = model.predict(df[['timestamp_unix','open','high','low','close','SMA10','Signal','SMA20']])
                    # signal = [1 if p[0] >= 0.5 else 0 for p in y]
                    # print(y)
                    cat = [1 if p[0] >= 0.5 else 0 for p in y]
                    # print(signal)
                    # print(cat)
                    # # print(signal)
                    if cat[0] == 1:
                        if signal[0] == 1:
                            st.info(f"Profitable Signal : You can BUY the stock of {choice}.")
                        elif signal[0] == 0:
                            st.info(f"Profitable Signal : You can SELL the stock of {choice}.")
                    elif cat[0] == 0:
                        st.warning(f"Non Profitable Signal : Dont BUY or SELL any stock of {choice}")
                else :
                    st.warning("Incorrect Input")
            elif model_choose == 'Random Forest Classification':
                # Load the pickled model
                with open(r"rfc.pkl", "rb") as model_file:
                    model = pickle.load(model_file)
                if signal[0] != None:
                    y = model.predict(df[['timestamp_unix','open','high','low','close','SMA10','Signal','SMA20']])
                    # signal = [1 if p[0] >= 0.5 else 0 for p in y]
                    # print(y)
                    # cat = [1 if p[0] >= 0.5 else 0 for p in y]
                    # print(signal)
                    # print(cat)
                    # # print(signal)
                    if y[0] == 1:
                        if signal[0] == 1:
                            st.info(f"Profitable Signal : You can BUY the stock of {choice}.")
                        elif signal[0] == 0:
                            st.info(f"Profitable Signal : You can SELL the stock of {choice}.")
                    elif y[0] == 0:
                        st.warning(f"Non Profitable Signal : Dont BUY or SELL any stock of {choice}")
                else :
                    st.warning("Incorrect Input")
                



