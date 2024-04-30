import json
from decimal import Decimal

from alpaca.trading.enums import OrderSide
from celery import shared_task
from celery.utils.log import get_task_logger

from . import helpers


logger = get_task_logger(__name__)


@shared_task
def bot_logic():
    config = json.loads(open("hello_azure/config.json").read())
    data = helpers.get_historical_price(config["Stock"],config["Key"],config["Secret"])
    print("Bot logic started")
    market_open = helpers.is_market_open(config["Key"],config["Secret"])

    #if Stock does not have an open position, then check account balance, size trade, check for crossover and place order
    position = helpers.get_open_position(config["Key"],config["Secret"],config["Stock"])
    if not position or config["Stock"] not in position.symbol:
        cash_balance = Decimal(helpers.get_account(config["Key"],config["Secret"]).cash)
        cash_position_size = (cash_balance * Decimal(config["Trade_Size"]))
        stock_price = Decimal(helpers.get_price(config["Key"],config["Secret"],config["Stock"]))
        shares_to_buy = int(cash_position_size / stock_price)
        shares_to_sell = position.qty_available if position else shares_to_buy

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
