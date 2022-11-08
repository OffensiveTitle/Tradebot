from ib_insync import *
import yfinance as yf
import time

# Const
ib = IB()
contract = Stock("AMD", "SMART", "USD")

# Placeholders
tradeStatus = True  # True = Buy, False = Sell
lastOpPrice = 0


# Funcs
def returnAveragePrice(period, stock=contract.symbol):
    stock = yf.Ticker(stock)
    stockHistory = stock.history(period=period)
    highAv = stockHistory["High"].mean()
    lowAv = stockHistory["Low"].mean()
    return round((highAv + lowAv) / 2, 2)


def numGen():
    return int(time.time())


def returnCurrentPrice(stock=contract.symbol):
    stock = yf.Ticker(stock)
    return stock.info["currentPrice"]


def returnAccountValue(tag="", currency=""):
    accountValueString = ib.accountValues()
    for a in accountValueString:
        if a.tag == tag and a.currency == currency:
            return float(a.value)


# Trading Sequence
def tryToTrade():
    global tradeStatus
    twoHundredDayAverage = returnAveragePrice('200d', contract.symbol)
    twentyOneDayAverage = returnAveragePrice('30d', contract.symbol)
    deviationRatio = twentyOneDayAverage / returnCurrentPrice()
    if deviationRatio > 1 and returnAccountValue(
            'CashBalance') > returnCurrentPrice() > twoHundredDayAverage and tradeStatus:
        placeBuyOrder()
        tradeStatus = False
    elif deviationRatio < 1:
        placeSellOrder()
        tradeStatus = True


def placeBuyOrder():
    f = open('logs.txt', 'a')
    f.write('Placing buy order. \n')
    f.close()
    nonce = numGen()
    buyOrder = MarketOrder("BUY", 1)
    buyOrder.orderId = nonce
    ib.qualifyContracts(contract)
    ib.placeOrder(contract, buyOrder)
    global lastOpPrice
    lastOpPrice = returnCurrentPrice()
    f = open('logs.txt', 'a')
    f.write(f'Placing buy order completed.\nPrice was {lastOpPrice}\nOrder ID is {nonce}.\n')
    f.close()


def placeSellOrder():
    f = open('logs.txt', 'a')
    f.write('Placing sell order. \n')
    f.close()
    nonce = numGen()
    sellOrder = MarketOrder("SELL", 1)
    sellOrder.orderId = nonce
    ib.qualifyContracts(contract)
    ib.placeOrder(contract, sellOrder)
    global lastOpPrice
    lastOpPrice = returnCurrentPrice()
    f = open('logs.txt', 'a')
    f.write(f'Placing sell order completed.\nPrice was {lastOpPrice}\nOrder ID is {nonce}.\n')
    f.close()


def runProgram():
    global tradeStatus
    tradeStatus = True
    while 1 > 0:
        t = time.localtime()
        if 15 >= t.tm_hour > 9 and not ib.isConnected():
            f = open('logs.txt', 'a')
            f.write("\nConnecting... \n")
            f.close()
            ib.connect(host="127.0.0.1", port=7497, clientId=1)
            t = time.localtime()
            while 15 >= t.tm_hour > 9 and ib.isConnected():
                t = time.localtime()
                tryToTrade()
                ib.sleep(259200)
            else:
                if ib.isConnected():
                    f = open('logs.txt', 'a')
                    f.write('Disconnecting...\n')
                    f.close()
                    ib.disconnect()
        ib.sleep(15)


runProgram()
