from celery import shared_task
from celery.utils.log import get_task_logger
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import yfinance as yf
from django.http import FileResponse
from io import BytesIO
import base64
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd 
import pytz
import pandas_market_calendars as mcal
import threading
import json 
from hello_azure import helpers
from alpaca.trading.enums import OrderSide
import time
from lightweight_charts import Chart
import pandas_ta as ta
from datetime import datetime, timedelta

logger = get_task_logger(__name__)


# @shared_task(ignore_result=True, time_limit=1)
# def add(x, y):
#     logger.info("Adding numbers")
#     return x + y


@shared_task
def bot_logic():
    config = json.loads(open("hello_azure/config.json").read())
    data = helpers.get_historical_price(config["Stock"],config["Key"],config["Secret"])
    response = ""
    #messages.info(request,'Bot logic started')
    print("Bot logic started")
    market_open = helpers.is_market_open(config["Key"],config["Secret"])

    #if Stock does not have an open position, then check account balance, size trade, check for crossover and place order
    if config["Stock"] not in helpers.get_open_position(config["Key"],config["Secret"],config["Stock"]).symbol:
        cash_balance = helpers.get_account(config["Key"],config["Secret"]).cash
        cash_position_size = (cash_balance * config["Trade_Size"]) 
        stock_price = helpers.get_price(config["Key"],config["Secret"],config["Stock"])
        shares_to_buy = cash_position_size / stock_price
        shares_to_sell = helpers.get_open_position(config["Key"],config["Secret"],config["Stock"]).qty_available

        sma1 = helpers.calculate_sma(data, config["SMA_1"])
        sma2 = helpers.calculate_sma(data, config["SMA_2"])
        
        if sma1 > sma2:
            order = helpers.place_market_order(config["Key"],config["Secret"],config["Stock"], shares_to_buy, OrderSide.BUY)
            print(order)
        elif sma2 > sma1:
            order = helpers.place_market_order(config["Key"],config["Secret"],config["Stock"], shares_to_sell, OrderSide.SELL)
            print(order)
        else:
            print(F"No Crossover yet, Current SMA {config['SMA_1']}: {sma1}, SMA {config['SMA_2']}: {sma2}")

        curr_price = helpers.get_price(config["Key"],config["Secret"],config["Stock"])
        data.loc[len(data)] = [0,0,0,curr_price,0,0,0,0,0]
    else:
        print((f"Already have an open position in: "
            f"{helpers.get_open_position(config['Key'],config['Secret'],config['Stock']).symbol} "
            f"| qty= "
            f"{helpers.get_open_position(config['Key'],config['Secret'],config['Stock']).qty} ")) 

    print("Bot logic finished")
    #return response, render(request, 'hello_azure/bot.html', {'response': response})
