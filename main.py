import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime
st.title("Forex-Market-Analysis")
choice = st.sidebar.selectbox("Select the Symbol",("EURUSD","AUDUSD","USDCHF"))
tf_choice = st.sidebar.selectbox("Select the Timeframe",("1 Min","5 Min","15 Min","30 Min","1 Hr","4 Hr","12 hr","Daily","Weekly","Monthly"))
from_date = st.sidebar.date_input("From :",value=None,format="DD.MM.YYYY")
to_date = st.sidebar.date_input("To :",value=None,format="DD.MM.YYYY")

if st.sidebar.button("Done"):
    print("Done")
    graph_choice = st.selectbox("Choose the Type of graph",("Candle Stick","Box plot","Scatter Plot","Histogram","Distribution Plot","Pie Chart","Line plot"))
    if choice == "EURUSD":
        # tf_choice = st.selectbox("Select the Timeframe",("1 Min","5 Min","15 Min","30 Min","1 Hr","4 Hr","12 hr","Daily","Weekly","Monthly"))
        if tf_choice == "1 Min":
            df = pd.read_csv(r"C:\Users\sitadmin\Desktop\Hevardhan\Forex-market-analysis\datasets\datasets\eurusd\eurusd_m1.csv")
            del df['Unnamed: 0']
            slider = st.number_input("Enter the Number of Rows to Display",value=10)       
            st.dataframe(df.head(slider))
            ddf = df.head(slider)
            if st.button("Show graph"):
                fig = go.Figure(data=[go.Candlestick(x=ddf['time'],
                    open=ddf['open'],
                    high=ddf['high'],
                    low=ddf['low'],
                    close=ddf['close'])])

                st.plotly_chart(fig)
            
#     if tf_choice == "5 Min":
#         df = pd.read_csv(r"C:\Users\sarav\Documents\EDA\datasets\eurusd\eurusd_m5.csv")
#         del df['Unnamed: 0']
#         slider = st.number_input("Enter the Number of Rows to Display",value=10)       
#         st.dataframe(df.head(slider))
#     if tf_choice == "15 Min":
#         df = pd.read_csv(r"C:\Users\sarav\Documents\EDA\datasets\eurusd\eurusd_m15.csv")
#         del df['Unnamed: 0']
#         slider = st.number_input("Enter the Number of Rows to Display",value=10)       
#         st.dataframe(df.head(slider))
#     if tf_choice == "30 Min":
#         df = pd.read_csv(r"C:\Users\sarav\Documents\EDA\datasets\eurusd\eurusd_m30.csv")
#         del df['Unnamed: 0']
#         slider = st.number_input("Enter the Number of Rows to Display",value=10)       
#         st.dataframe(df.head(slider))
#     if tf_choice == "1 Hr":
#         df = pd.read_csv(r"C:\Users\sarav\Documents\EDA\datasets\eurusd\eurusd_h1.csv")
#         del df['Unnamed: 0']
#         slider = st.number_input("Enter the Number of Rows to Display",value=10)       
#         st.dataframe(df.head(slider))
#     if tf_choice == "4 Hr Min":
#         df = pd.read_csv(r"C:\Users\sarav\Documents\EDA\datasets\eurusd\eurusd_h4.csv")
#         del df['Unnamed: 0']
#         slider = st.number_input("Enter the Number of Rows to Display",value=10)       
#         st.dataframe(df.head(slider))

