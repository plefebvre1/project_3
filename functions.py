# Imports and dependencies
import pandas as pd
import numpy as np
from pathlib import Path
import os
import json
import requests
from dotenv import load_dotenv
from td.client import TDClient
import datetime as dt
import hvplot.pandas
import plotly.express as px



load_dotenv()


# Load api key and api redirect uri; set json path
CLIENT_ID = os.getenv('CLIENT_ID')
REDIRECT_URI = os.getenv('REDIRECT_URI')
CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH')

# Login to TDSession
TDSession = TDClient(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    credentials_path=CREDENTIALS_PATH
)

TDSession.login()

# Pulls market data using the TD Ameritrade API and formats the data
def pull_market_data(stock_ticker, number_of_periods):
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}'
    full_url = endpoint.format(stock_ticker=stock_ticker,periodType='year',period=number_of_periods,frequencyType='daily')
    page = requests.get(url=full_url, params={'apikey' : CLIENT_ID})
    content = json.loads(page.content)
    market_data = pd.DataFrame(content['candles'])
    market_data['datetime'] = market_data['datetime']/1000
    market_data['datetime'] = market_data['datetime'].apply(dt.datetime.fromtimestamp)
    market_data['datetime'] = market_data['datetime'].dt.date
    market_data = market_data.set_index('datetime')
    market_data.drop(["open", "high", "low", "volume"], axis=1, inplace=True)
    market_data.dropna(inplace=True)

    return market_data

# Format the ameritrade account balance CSV file
def format_ameritrade_export(file_path):
    portfolio_data = pd.read_csv(
        Path(file_path)
    )

    portfolio_data.rename(columns = {"Account value": "value"}, inplace=True)
    portfolio_data.dropna(inplace=True)
    portfolio_data["Date"] = pd.to_datetime(portfolio_data["Date"], format = '%m/%d/%Y')
    portfolio_data.set_index("Date", inplace = True)
    #portfolio_data["value"] = portfolio_data["value"].str.replace(',', '')
    portfolio_data["value"] = portfolio_data["value"].astype(float, errors = 'raise')
    portfolio_data.dropna(inplace=True)
    
    return portfolio_data

# Calculates statistics on the market and the portfolio
def get_statistics(portfolio_data, spy_data, rf):
    statistics = ["daily_returns", "cumulative_returns", "average_annualized_returns", "volatility", "variance", "covariance", "annualized_sharpe_ratio"] 
    portfolio_statistics = [] 
    market_statistics = []
    rows = ["portfolio", "market"]
    
    daily_returns = portfolio_data["value"].pct_change()
    spy_daily_returns = spy_data["close"].pct_change()
    portfolio_statistics.append(daily_returns)
    market_statistics.append(spy_daily_returns)
    
    cum_returns = (1+daily_returns).cumprod()
    spy_cum_returns = (1+spy_daily_returns).cumprod()
    portfolio_statistics.append(cum_returns)
    market_statistics.append(spy_cum_returns)
    
    average_annualized_returns = daily_returns.mean() * 252
    average_annualized_market_returns = spy_daily_returns.mean() * 252
    portfolio_statistics.append(average_annualized_returns)
    market_statistics.append(average_annualized_market_returns)
    
    volatility = portfolio_data["value"].std()
    market_volatility = spy_daily_returns.std()
    portfolio_statistics.append(volatility)
    market_statistics.append(market_volatility)
    
    variance = daily_returns.var()
    market_variance = spy_daily_returns.var()
    portfolio_statistics.append(variance)
    market_statistics.append(market_variance)
    
    covariance = daily_returns.cov(spy_daily_returns)
    portfolio_statistics.append(covariance)
    market_statistics.append(covariance)
    
    annualized_volatility = volatility * np.sqrt(252)
    annualized_market_volatility = market_volatility * np.sqrt(252)
    sharpe_ratio = average_annualized_returns - rf / annualized_volatility
    market_sharpe_ratio = average_annualized_market_returns - rf / annualized_market_volatility
    portfolio_statistics.append(sharpe_ratio)
    market_statistics.append(market_sharpe_ratio)
    
    main = [statistics, portfolio_statistics, market_statistics]
    
    summary = pd.DataFrame({'statistics': statistics[2:7], 'portfolio_statistics' : portfolio_statistics[2:7], 'market_statistics' : market_statistics[2:7]}).set_index('statistics')
    
    plot_1 = market_statistics[1].hvplot.line(
        subplots=True,
        xlabel='Date',
        ylabel='Cumulative Return',
        color="lightgrey",
        height=500,
        width=1000,
        label = "Selected Stock"
    ).opts(
        yformatter='%.2f',
        line_color="blue",
        hover_line_color="green",
    )
    plot_2 = portfolio_statistics[1].hvplot.line(
        subplots=True,
        xlabel='Date',
        ylabel='Cumulative Return',
        label = "Portfolio",
        color="lightgrey",
        height=500,
        width=1000,
    ).opts(
        yformatter='%.2f',
        line_color="purple",
        hover_line_color="yellow"
    )

    #fig = px.line(portfolio_statistics,x = 'date', y = 'cum_returns')

    plot = ""

    return summary, plot


