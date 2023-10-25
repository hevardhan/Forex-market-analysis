import streamlit as st
import MetaTrader5 as mt5

# Streamlit app title
st.title("MetaTrader 5 Initialization")

# Initialize MetaTrader 5
if st.button("Initialize MetaTrader 5"):
    # Initialize MT5 connection
    mt5.initialize()

    # Check if initialization was successful
    if not mt5.initialize():
        st.error("MetaTrader 5 Initialization Failed")
    else:
        st.success("MetaTrader 5 Initialized Successfully")

# Streamlit app clean-up (optional)
st.text("You can perform other tasks here.")
st.warning("Remember to properly close MT5 when you're done.")

# Close MetaTrader 5 connection (optional)
if st.button("Close MetaTrader 5"):
    mt5.shutdown()
    st.success("MetaTrader 5 Connection Closed")
