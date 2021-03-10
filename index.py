import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.005
closes = []
in_postion = False

client = Client(config.API_KEY, config.API_SECRET)

quatitiyToTrade = 1
currentBuyPrice = 0
profitMade = []

def order(symbol, quantity, side, order_type=ORDER_TYPE_MARKET):
    order = client.create_order(symbol=symbol,
    side=side,
    type=order_type,
    quantity=quantity)

def on_open(ws):
    print('open')

def on_close(ws):
    print('close')

def on_message(ws, message):
    json_message = json.loads(message)
    #print('message received', pprint.pprint(json_message))
    candle = json_message['k']

    is_candle_closed = candle['x']
    #print(candle)
    close = candle['c']
    print('close',close)

    if is_candle_closed:
        print('candle closed at {}'.format(close))
        closes.append(float(close))
        #
        print('Closes',closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("RSI List :",rsi)
            last_rsi = rsi[-1]
            print("Current RSI is {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_postion:
                    print("Sold at :",closes[-1])
                    in_postion = False
                    profitMade.append((closes[-1] - currentBuyPrice))
                    print("Profit Made: ",profitMade[-1])
                    print("Total Profit Made :", sum(profitMade))
                    print("Profit Arrray :", profitMade)
                    # put binance sell logic here
                else:
                    print("It is overbought, but we don't own any. Nothing to do.")
            
            if last_rsi < RSI_OVERSOLD :
                if in_postion:
                    print("It is oversold, but you already own it, nothing to do")
                else:
                    print("Bought at :",closes[-1])
                    in_postion = True
                    currentBuyPrice = closes[-1]
                    # Buy Logic

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

ws.run_forever()