"""
Helpers for SMA Bot
Name: Muhammad Moaz
Email: mujahidmoaz@gmail.com
"""

# Import Libraries
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

    end = datetime.now()- timedelta(days=(1))
    start = end - timedelta(days=(90))

    # Creating request object
    request_params = StockBarsRequest(
        symbol_or_symbols=[stock],
        timeframe=TimeFrame.Day,
        start=start,
        end=end
    )

    data = client.get_stock_bars(request_params)

    # Convert to dataframe and save in csv
    data.df.to_csv("hello_azure/history/{}.csv".format(stock))
    return data.df

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
    position = trading_client.get_open_position(symbol_or_asset_id=symbol)

    return position


def is_market_open(key, secret):
    # trading_client = TradingClient(key, secret, paper=True)
    # calendar = trading_client.get_calendar()
    # now = datetime.now()
    # for session in calendar.sessions:
    #     if session.start <= now() <= session.end:
    #         return True
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