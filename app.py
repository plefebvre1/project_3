# Imports and requirements
import os
import json
import requests
from dotenv import load_dotenv
from td.client import TDClient
import streamlit as st
from functions import pull_market_data, format_ameritrade_export, get_statistics
import holoviews as hv
hv.extension('bokeh', logo=False)
import matplotlib.pyplot as plt

# Load local environment variables
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
REDIRECT_URI = os.getenv('REDIRECT_URI')
CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH')

# Initiate TDSession
TDSession = TDClient(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    credentials_path=CREDENTIALS_PATH
)

TDSession.login()

# Add a title for the page
st.markdown("## TD Ameritrade Account Metrics")
st.markdown("### Use this site to compare your account to any desired market account or ticker.")

# Streamlit user inputs
account_path = st.text_input("Account File Path")
market_ticker = st.text_input("Market Ticker")
period_options = (1,2,3,5,10,15,20)
time_period = st.selectbox("Time Period (years)",period_options)



# Add a button using Streamlit to run functions
if st.button("Compare"):
    # risk free rate
    rf = 0.007
    # Call custom functions
    market_data = pull_market_data(market_ticker,time_period)
    account_data = format_ameritrade_export(account_path)
    summary_df, plot = get_statistics(account_data,market_data,rf)
    st.write(summary_df)
    st.plotly_chart(plot)
