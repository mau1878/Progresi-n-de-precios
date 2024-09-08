import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Set Streamlit layout
st.set_page_config(layout="wide")

# Title
st.title('Stock Value Progression Over Time')

# Sidebar for inputs
st.sidebar.header('User Input')
tickers = st.sidebar.text_input('Enter stock tickers (separated by commas)', 'AAPL,MSFT,GOOGL')
start_date = st.sidebar.date_input('Select start date', pd.to_datetime('2020-01-01'))
end_date = st.sidebar.date_input('Select end date', pd.to_datetime('today'))

# Convert tickers to list and trim spaces
tickers = [ticker.strip().upper() for ticker in tickers.split(',')]

# Fetch data from yfinance
@st.cache
def fetch_data(tickers, start_date, end_date):
    return yf.download(tickers, start=start_date, end=end_date)['Adj Close']

# Fetch and show progress
with st.spinner('Fetching data...'):
    stock_data = fetch_data(tickers, start_date, end_date)

# Remove missing data
stock_data = stock_data.dropna()

# Prepare data for animation
stock_data = stock_data.reset_index()
stock_data = stock_data.melt(id_vars='Date', value_vars=tickers, var_name='Ticker', value_name='Value')

# Create animated bar plot using Plotly
fig = px.bar(
    stock_data,
    x='Ticker',
    y='Value',
    color='Ticker',
    animation_frame='Date',
    range_y=[0, stock_data['Value'].max() * 1.1],
    title='Stock Value Progression Over Time',
    labels={'Value': 'Stock Value (Adjusted Close)', 'Date': 'Date'},
    template='plotly_white'
)

# Display the plot
st.plotly_chart(fig, use_container_width=True)
