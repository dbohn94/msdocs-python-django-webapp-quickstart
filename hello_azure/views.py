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

#Index view: URL Endpoint index, HTTP method (GET by default)
#Behavior: prints a message to the console indicating that a request for the index page has been recieved and then renders an HTML template named 'hello_azure/index.html' using the render function.
#The rendered HTML is then sent as the HTTP response 
def index(request):
    print('Request for index page received')
    return render(request, 'hello_azure/index.html')


def bot_logic(request):
        config = json.loads(open("hello_azure/config.json").read())
        data = helpers.get_historical_price(config["Stock"],config["Key"],config["Secret"])
        response = ""
        messages.info(request,'Bot logic started')
        #open_positions = helpers.get_open_position(config["Key"],config["Secret"],config["Stock"]).symbol
        #print(f"Open positions: {open_positions}")

        if config["Stock"] not in helpers.get_open_position(config["Key"],config["Secret"],config["Stock"]).symbol:
            while True:
                sma1 = helpers.calculate_sma(data, config["SMA_1"])
                sma2 = helpers.calculate_sma(data, config["SMA_2"])
                
                if sma1 > sma2:
                    order = helpers.place_market_order(config["Key"],config["Secret"],config["Stock"], config["Qty"], OrderSide.BUY)
                    print(order)
                elif sma2 > sma1:
                    order = helpers.place_market_order(config["Key"],config["Secret"],config["Stock"], config["Qty"], OrderSide.SELL)
                    print(order)
                else:
                    print(F"No Crossover yet, Current SMA {config['SMA_1']}: {sma1}, SMA {config['SMA_2']}: {sma2}")
                    break
                curr_price = helpers.get_price(config["Key"],config["Secret"],config["Stock"])
                data.loc[len(data)] = [0,0,0,curr_price,0,0,0,0,0]
        else:
            print((f"Already have an open position in: "
                f"{helpers.get_open_position(config['Key'],config['Secret'],config["Stock"]).symbol} "
                f"| qty= "
                f"{helpers.get_open_position(config['Key'],config['Secret'],config["Stock"]).qty} ")) 
            time.sleep(300)
        return response, render(request, 'hello_azure/bot.html', {'response': response})

def bot(request):
    response = bot_logic(request) # Run the bot_logic function
    return render(request, 'hello_azure/bot.html', {'response': response})  # Pass the result to the template


#hello view: handles both GET and POST requests 
#Behavior: POST, retrieves the value of the 'name' parameter from the POST data
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
    #df = yf.download('SPY', period='1d', interval='1m')  # Fetch data
    #df = yf.download('SPY', interval='5m', start='2023-12-01', end='2023-12-31')
    df = yf.download('SPY', interval='5m', period='1mo')
    # Convert the index to Eastern Time
    df.index = df.index.tz_convert('US/Eastern')
    # Exclude weekends
    df = df[df.index.weekday < 5]

    # Get the NYSE calendar
    nyse = mcal.get_calendar('NYSE')

    # Get market holidays
    holidays = nyse.holidays().holidays

    # Exclude holidays
    df = df[~pd.Series(df.index.date, index=df.index).isin(holidays)]
    # Drop rows with NaN values
    df = df.dropna()

    # Calculate 10-day SMA
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    
    #Create first chart
    df2 = df 
    df2['Date'] = df2.index
    # plotly candlestick figure
    fig = go.Figure(data=[go.Candlestick(
        x=df2['Date'],
        open=df2['Open'], high=df2['High'],
        low=df2['Low'], close=df2['Close'],
    )])

    # grab first and last observations from df.date and make a continuous date range from that
    dt_all = pd.date_range(start=df2['Date'].iloc[0],end=df2['Date'].iloc[-1], freq = '5min')

    # check which dates from your source that also accur in the continuous date range
    dt_obs = [d.strftime("%Y-%m-%d %H:%M:%S") for d in df2['Date']]

    # isolate missing timestamps
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d %H:%M:%S").tolist() if not d in dt_obs]
    dt_breaks = pd.to_datetime(dt_breaks)

    fig.update_xaxes(rangebreaks=[dict(dvalue = 5*60*1000, values=dt_breaks)] )

    
    # Create second chart
    fig2 = go.Figure(data=go.Ohlc(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close']))
    

    # Add SMA to the chart
    fig2.add_trace(go.Scatter(x=df.index, y=df['SMA_10'], mode='lines', name='SMA 10'))
    fig2.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], mode='lines', name='SMA 50'))

    fig2.update_layout(
    autosize=False,
    width=1200,  # Adjust the width of the chart
    height=1000,  # Adjust the height of the chart
    margin=dict(
        l=50,  # left margin
        r=50,  # right margin
        b=100,  # bottom margin
        t=100,  # top margin
        pad=10
    ),
    font=dict(
        size=12,
    )
)
    # Convert the first chart to HTML
    chart1 = plot(fig, output_type='div')
    # Convert the second chart to HTML
    chart2 = plot(fig2, output_type='div')
    # Convert the DataFrame to HTML
    df_html = df.head(100).to_html()

    return render(request, 'hello_azure/spy_chart.html', {'chart1':chart1, 'chart2': chart2, 'df_html':df_html}) 