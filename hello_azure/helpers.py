"""
Helpers for SMA Bot
Name: Muhammad Moaz
Email: mujahidmoaz@gmail.com
"""

import pytz
from alpaca.common.exceptions import APIError
from alpaca.data.requests import StockBarsRequest, StockLatestQuoteRequest
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import TimeInForce
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

def get_historical_price(stock, api, secret):
    """
    Get 90 days historical price of a stock

    Args: stock(str) -> stock of which historical data is needed
          api (str) -> API key of alpaca
          secret (str) -> secret key of alpaca

    Returns: data (DataFrame) -> Historical data
    """
    client = StockHistoricalDataClient(
        api_key=api, secret_key=secret)

    end = datetime.now(pytz.timezone('US/Eastern')) - timedelta(days=(1))
    start = end - timedelta(days=(90))

    # Creating request object
    request_params = StockBarsRequest(
        symbol_or_symbols=[stock],
        timeframe=TimeFrame.Day,
        start=start,
        end=end
    )

    data = client.get_stock_bars(request_params)

    return data.df

def get_historical_price_30min(stock, api, secret):
    """
    Get 14 days historical price of a stock by the minute
    Returns: data (DataFrame) -> Historical data 30 min
    """
    client = StockHistoricalDataClient(
        api_key=api, secret_key=secret)

    end = datetime.now(pytz.timezone('US/Eastern')) - timedelta(days=(1))
    start = end - timedelta(days=(14))

    # Creating request object
    request_params = StockBarsRequest(
        symbol_or_symbols=[stock],
        timeframe=TimeFrame.Minute,
        start=start,
        end=end
    )

    bars = client.get_stock_bars(request_params)
    
    # Convert to dataframe
    df = bars.df

    # Remove after hours data
    datac = df[(df.index.get_level_values(1).hour <=16)]
    datad = datac[(datac.index.get_level_values(1).hour >=9)]
    
    # Get only :00 and :30 values
    data30 = datad[(datad.index.get_level_values(1).minute == 0) | (datad.index.get_level_values(1).minute == 30)].copy()
    
    return data30

def get_price(api, secret, symbol):
    """
    Get Latest price of a symbol

    Args: 
        api (str) -> API key of alpaca
        secret (str) -> secret key of alpaca
        symbol (str) -> symbol of which the latest price is needed

    Returns: (float) -> latest price of the requested symbol
    """
    client = StockHistoricalDataClient(
        api_key=api, secret_key=secret)
    try:
        latest_quote = client.get_stock_latest_quote(StockLatestQuoteRequest(symbol_or_symbols=symbol))
        return latest_quote[symbol].ask_price
    except:
        return None

    
def calculate_sma(data, window):
    windows = data["close"].rolling(window)
    data[f"SMA {window}"] = windows.mean().tolist()
    return data[f"SMA {window}"].iloc[-1]


def place_market_order(key, secret, stock, qty, side):
    """
    Function to place order on alpaca 

    Args: stock(str) -> stock of which historical data is needed
          api (str) -> API key of alpaca
          secret (str) -> secret key of alpaca
          qty (int) -> quantity of stocks to be bought or sold
          side (str) -> side of the order (buy or sell)

    Returns: market order object of the placed order
    """
    trading_client = TradingClient(key, secret, paper=True)
    market_order = trading_client.submit_order(
        order_data=MarketOrderRequest(
            symbol=stock,
            qty=qty,
            side=side,
            time_in_force=TimeInForce.GTC
        )
    )

    return market_order

def get_open_position(key, secret, symbol):
    trading_client = TradingClient(key, secret, paper=True)

    try:
        position = trading_client.get_open_position(symbol_or_asset_id=symbol)
        return position
    except APIError:
        # Throws an APIError if the position does not exist.
        return None


def is_market_open(key, secret):
    trading_client = TradingClient(key, secret, paper=True)
    calendar = trading_client.get_calendar()
    tz = pytz.timezone('US/Eastern')
    now = datetime.now(tz)
    for session in calendar:
        if tz.localize(session.open) <= now <= tz.localize(session.close):
            return True
    return False


def get_account(key, secret):
    trading_client = TradingClient(key, secret, paper=True)
    account = trading_client.get_account()
    return account

# Function to write log file
def write_log(log):
    """
    Write log in a txt file

    Args: log (str) -> log to append into the file

    Returns: None
    """
    with open("Log.txt", "a") as f:
        f.write(log + "\n")
        f.close()
