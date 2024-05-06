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

from .models import DecisionLog, TradeLog, DecisionSummary


#Index view: URL Endpoint index, HTTP method (GET by default)
#Behavior: prints a message to the console indicating that a request for the index page has been recieved and then renders an HTML template named 'hello_azure/index.html' using the render function.
#The rendered HTML is then sent as the HTTP response 
def index(request):
    print('Request for index page received')
    return render(request, 'hello_azure/index.html')


def bot(request):
    response = bot_logic(request) # Run the bot_logic function
    return render(request, 'hello_azure/bot.html', {'response': response})  # Pass the result to the template

@csrf_exempt
def hello(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if name is None or name == '':
            print("Request for hello page received with no name or blank name -- redirecting")
            return redirect('index')
        else:
            print("Request for hello page received with name=%s" % name)
            context = {'name': name }
            return render(request, 'hello_azure/hello.html', context)
    else:
        return redirect('index')

#spy_chart view: URL Endpoint spy_chart, HTTP method (GET by default)
def spy_chart(request):
    # Fetch the last 14 days 336 hours of SPY data with 30-minute bars
    now = datetime.now(pytz.timezone('US/Eastern'))
    start_date = now - timedelta(hours=24*14)
    spy = yf.Ticker("SPY")
    data = yf.download('SPY', start=start_date, interval='30m')
    data['Open'] = data['Open'].round(2)
    data['High'] = data['High'].round(2)
    data['Low'] = data['Low'].round(2)
    data['Close'] = data['Close'].round(2)
    data['Adj Close'] = data['Adj Close'].round(2)
    data['sma_10'] = data['Close'].dropna().rolling(window=10, min_periods=1).mean()
    data['sma_50'] = data['Close'].dropna().rolling(window=50, min_periods=1).mean()
    # this library expects lowercase columns for date, open, high, low, close, volume
    data = data.reset_index()
    data.columns = data.columns.str.lower()
    data['time'] = data['datetime'].map(lambda x: int(round(x.timestamp())))

    # Convert the DataFrame to a dictionary
    candlestick_data = data[['time', 'open', 'high', 'low', 'close']].reset_index().to_dict(orient='records')
    sma10_data = data.rename(columns={"sma_10": "value"})[['time', 'value']].reset_index().to_dict(orient='records')
    sma50_data = data.rename(columns={"sma_50": "value"})[['time', 'value']].reset_index().to_dict(orient='records')

    print(data.head(100))
    # Sort the DataFrame by Datetime DESC
    df_html_sort = data.sort_values(by='time', ascending=False)
    # Convert the DataFrame to HTML
    df_html = df_html_sort.head(100).to_html()

    decisions_cutoff = now - timedelta(hours=2)
    decisions = DecisionLog.objects.filter(timestamp__gte=decisions_cutoff).order_by("-timestamp")
    decisions2 = DecisionSummary.objects.all().order_by("-timestamp")
    trades = TradeLog.objects.all().order_by("-timestamp")

    return render(request, 'hello_azure/spy_chart.html', {
        'candlestick_data': json.dumps(candlestick_data),
        'sma10_data': json.dumps(sma10_data),
        'sma50_data': json.dumps(sma50_data),
        'decisions': decisions,
        'decisions2': decisions2,
        'trades': trades,
        'df_html': df_html
    })
