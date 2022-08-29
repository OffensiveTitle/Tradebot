from ib_insync import *
import yfinance as yf
import time
import pandas as pd

#Const
IB = IB()
CONTRACT = Stock("AMD", "SMART", "USD")

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
    sevenDayAverage = returnAveragePrice("7d", "AMD")
    twentyOneDayAverage = returnAveragePrice("21d", "AMD")
    if sevenDayAverage < twentyOneDayAverage and returnBalance() > returnCurrentPrice():
        placeBuyOrder()
    elif sevenDayAverage > twentyOneDayAverage:
        placeSellOrder()

def placeBuyOrder():
    print("Placing buy order. \n")
    NONCE = numGen()
    buyOrder = MarketOrder("BUY", 1)
    buyOrder.orderId = NONCE
    IB.qualifyContracts(CONTRACT)
    IB.placeOrder(CONTRACT, buyOrder)
    global lastOpPrice
    lastOpPrice = returnCurrentPrice()
    print(f"Placing buy order completed.\nPrice was {lastOpPrice}\nOrder ID is {NONCE}.\n")
def placeSellOrder():
    print("Placing sell order. \n")
    NONCE = numGen()
    sellOrder = MarketOrder("SELL", 1)
    sellOrder.orderId = NONCE
    IB.qualifyContracts(CONTRACT)
    IB.placeOrder(contract, sellOrder)
    global lastOpPrice
    lastOpPrice = returnCurrentPrice()
    print(f"Placing sell order completed.\nPrice was {lastOpPrice}\nOrder ID is {NONCE}.\n")

def runProgram():
    print("Connecting... \n")
    IB.connect(host="127.0.0.1", port="7497", clientId=2)
    while(1>0):
        tryToTrade()
        IB.sleep(30)

runProgram()