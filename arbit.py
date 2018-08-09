###################Importing modules####################
import requests
import json
import time
import os
########################################################

####################Config Variables####################
minVol = 200 #Minimum volume (In BTC) an exchange should have to be taken into account by this program
exchangedToIgnore = ["hitbtc", "indacoin"]
substitutedNames = {"PINK-btc":"pc-btc"}
########################################################

def getCoinNames(minVol):
  from poloniex import Poloniex
  api =  Poloniex()
  coinList = []
  coins = api.return24hVolume()
  for market in coins:
    if "BTC_" in market and float(coins[market]["BTC"]) > minVol:
      coinList.append(market.replace("BTC_","") + "-btc")
  coinList = [substitutedNames[x] if x in substitutedNames else x for x in coinList]
  return coinList

################Function gets market list###############
def getMarketList(pair):
    try:
        output = requests.get("https://api.cryptonator.com/api/full/" + pair).json()
        print("1")
        time.sleep(31)
    except:
        return None
        
    #print(json.loads(output.content))
    
    
    if output == None:
        return None
    markets = output["ticker"]["markets"]
    
    return markets
########################################################

######Function finds lowest and highest exchanges#######
def getLowestHighestMarkets(exchangedToIgnore, minVol, markets):
    lowestMarket = {"price": 10000000000, "volume": 0}
    highestMarket = {"price": 0, "volume": 0}
    for market in markets:
        if market["market"].lower() not in exchangedToIgnore:
            market["price"] = marketPrice = float(market["price"])
            market["volume"] = marketVolume = market["volume"] * market["price"]
            
            if float(marketVolume) >= minVol:
                if marketPrice < lowestMarket["price"]:
                    lowestMarket = market

                if marketPrice > highestMarket["price"]:
                    highestMarket = market
        
    return {"lowestMarket" : lowestMarket, "highestMarket" : highestMarket}
########################################################
            
###############Function calculates stats################
def calcStats(lowestHighestMarkets, pair):
    lowestMarket = lowestHighestMarkets["lowestMarket"]
    highestMarket = lowestHighestMarkets["highestMarket"]
    exchangeUrls = {'wexnz':'https://wex.nz','yobit' : 'http://yobit.net', 'indacoin' : 'http://indacoin.com', 'kuna' : 'http://en.kuna.com.ua', 'bitstamp' : 'http://bitstamp.net', 'btc-e' : 'http://btc-e.com', 'bittrex' : 'http://bittrex.com', 'cex' : 'http://cex.io', 'http://bleutrade' : 'http://bleutrade.com', 'exmo' : 'http://exmo.com', 'hitbtc' : 'http://hitbtc.com', 'poloniex' : 'http://poloniex.com', 'bitfinex' : 'http://bitfinex.com', 'livecoin' : 'http://livecoin.net', 'c-cex' : 'http://c-cex.com', 'kraken' : 'http://kraken.com'}
    
    baseCurrency = pair[-3:]
    potentialGainPercent = round(highestMarket["price"] / (lowestMarket["price"] / 100) - 100, 3)
    try:
        lowestExchangeUrl = exchangeUrls[lowestMarket["market"].lower()]
        highestExchangeUrl = exchangeUrls[highestMarket["market"].lower()]

        #lowestExchangeUrl ='asd'
        #highestExchangeUrl = 'wew'
        #lowestExchange = lowestMarket["market"]
        #highestExchange = highestMarket["market"]
    
        lowestPrice = lowestMarket["price"]
        highestPrice = highestMarket["price"]
    except Exception as e:
        return {"pair" : pair, "baseCurrency" : baseCurrency, "potentialGainPercent" : potentialGainPercent, "lowestExchangeUrl" : 0.0, "highestExchangeUrl" : 0.0, "lowestPrice" : 0.0, "highestPrice" : 0.0}        

    return {"pair" : pair, "baseCurrency" : baseCurrency, "potentialGainPercent" : potentialGainPercent, "lowestExchangeUrl" : lowestExchangeUrl, "highestExchangeUrl" : highestExchangeUrl, "lowestPrice" : lowestPrice, "highestPrice" : highestPrice}
########################################################

#####################Run Functions######################
def getCoinStats():
    coinStats = []
    coinNames = getCoinNames(minVol)
    print(coinNames)
    print(len(coinNames))
    #import os
    
    for coin in coinNames:  
        #os.system("clear")
        #os.system("clear")
        print(str(round(100 / (len(coinNames) / (coinNames.index(coin) + 1)), 1)) + "%")
        markets = getMarketList(coin)
        arbitrageStats = {}
        arbitrageStats["potentialGainPercent"] = 0
        if markets != None:
            lowestHighestMarkets = getLowestHighestMarkets(exchangedToIgnore, minVol, markets)
            arbitrageStats = calcStats(lowestHighestMarkets, coin)
        if arbitrageStats["potentialGainPercent"] > 0:
            coinStats.append(arbitrageStats)
    return coinStats
########################################################
coinStats = getCoinStats()
#os.system("clear")
#os.system("clear")
#print(coinStats)
print(len(coinStats))
for coin in sorted(coinStats, key=lambda k: k['potentialGainPercent']):
    stats = coin
    print("\n")
    print("Pair: " + stats["pair"])
    if(type(stats["lowestPrice"]) == "str"):
       stats["lowestPrice"] = float(stats["lowestPrice"])
    if(type(stats["highestPrice"]) == "str"):
       stats["highestPrice"] = float(stats["highestPrice"])
    print("Buy at " + stats["lowestExchangeUrl"] + " for " + format(stats["lowestPrice"], '.8f') + " " + stats["baseCurrency"].upper())
    print("Sell at " + stats["highestExchangeUrl"] + " for " + format(stats["highestPrice"], '.8f') + " " + stats["baseCurrency"].upper())
    print("Potential gain: " + str(stats["potentialGainPercent"]) + "%")

########################################################
