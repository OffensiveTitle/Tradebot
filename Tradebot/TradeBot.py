from ib_insync import *
import yfinance as yf
import time


#Const
IB = IB()
CONTRACT = Stock("AMD", "SMART", "USD")
f = open('logs.txt', 'a')

#Placeholders
NONCE = 0
sevenDayAverage = 0
twentyOneDayAverage = 0

#Funcs
def returnAveragePrice(period = "7d", stock = "AMD"):
    stock = yf.Ticker(stock)
    stockHistory = stock.history(period=period)
    highAv = stockHistory["High"].mean()
    lowAv = stockHistory["Low"].mean()
    return round((highAv + lowAv)/2, 2)
def numGen ():
    return int(time.time())
def returnCurrentPrice(stock = "AMD"):
    stock = yf.Ticker(stock)
    return stock.info["currentPrice"]
def returnBalance():
    accountBalanceString = IB.accountSummary()
    for a in accountBalanceString:
	    if a.tag=="AvailableFunds":
		    return float(a.value)

#Trading Sequence
def tryToTrade():
    sevenDayAverage = returnAveragePrice("7d", CONTRACT.symbol)
    twentyOneDayAverage = returnAveragePrice("21d", CONTRACT.symbol)
    if sevenDayAverage < twentyOneDayAverage and returnBalance() > returnCurrentPrice():
        placeBuyOrder()
    elif sevenDayAverage > twentyOneDayAverage:
        placeSellOrder()

def placeBuyOrder():
    f = open('logs.txt', 'a')
    f.write('Placing buy order. \n')
    f.close()
    NONCE = numGen()
    buyOrder = MarketOrder("BUY", 1)
    buyOrder.orderId = NONCE
    IB.qualifyContracts(CONTRACT)
    IB.placeOrder(CONTRACT, buyOrder)
    global lastOpPrice
    lastOpPrice = returnCurrentPrice()
    f = open('logs.txt', 'a')
    f.write(f'Placing buy order completed.\nPrice was {lastOpPrice}\nOrder ID is {NONCE}.\n')
    f.close()
def placeSellOrder():
    f = open('logs.txt', 'a')
    f.write('Placing sell order. \n')
    f.close()
    NONCE = numGen()
    sellOrder = MarketOrder("SELL", 1)
    sellOrder.orderId = NONCE
    IB.qualifyContracts(CONTRACT)
    IB.placeOrder(contract, sellOrder)
    global lastOpPrice
    lastOpPrice = returnCurrentPrice()
    f = open('logs.txt', 'a')
    f.write(f'Placing sell order completed.\nPrice was {lastOpPrice}\nOrder ID is {NONCE}.\n')
    f.close()

def runProgram():
    f = open('logs.txt', 'a')
    f.write("\nConnecting... \n")
    f.close()
    IB.connect(host="127.0.0.1", port="7497", clientId=1)
    t = time.localtime()
    while(t.tm_hour <= 15 and t.tm_hour > 9):
        t = time.localtime()
        tryToTrade()
        IB.sleep(86400)
    else:
        f = open('logs.txt', 'a')
        f.write('Disconnecting...\n')
        f.close()
        IB.disconnect()


runProgram()