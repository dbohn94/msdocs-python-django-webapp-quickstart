"""
SMA Stock Market bot Alpaca 
Name: Muhammad Moaz
Email: mujahidmoaz@gmail.com
"""

# Import Libraries
import json
import helpers
from alpaca.trading.enums import OrderSide
import time

config = json.loads(open("config.json").read())

data = helpers.get_historical_price(config["Stock"],config["Key"],config["Secret"])

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
    
    time.sleep(300)
    curr_price = helpers.get_price(config["Key"],config["Secret"],config["Stock"])
    data.loc[len(data)] = [0,0,0,curr_price,0,0,0,0,0]

    
