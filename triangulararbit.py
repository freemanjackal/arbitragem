
import requests
import json
from binance.client import Client

"""
headers= {'Accept': 'application/json', 'User-Agent': 'binance/python', 'X-MBX-APIKEY': '5ZskPFW3CeJEpbWItVTrPsy2ngSn3d1ued0cOH2kHipVuIhkMfETgxRN8Ljzrv9Q'}
tickers = requests.get("https://api.binance.com/api/v1/ticker/24hr", headers=headers)
"""

client = Client('5ZskPFW3CeJEpbWItVTrPsy2ngSn3d1ued0cOH2kHipVuIhkMfETgxRN8Ljzrv9Q', 'tCsChD24BHmLjqSVcYFgY1TzPKLji9OAzVlJdQlSPhL7t2O8PDwWFhrkbhVqyuvA')
#depth = client.get_order_book(symbol='ETHBTC')
tickers = client.get_ticker(symbol='ETHBTC')

tickers = client.get_orderbook_tickers()
ticker = client.get_orderbook_ticker()
prices = client.get_all_tickers()

btc = 0.02/0.07762800

print(prices)
