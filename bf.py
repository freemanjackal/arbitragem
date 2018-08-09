"""
The Bellman-Ford algorithm
Graph API:
    iter(graph) gives all nodes
    iter(graph[u]) gives neighbours of u
    graph[u][v] gives weight of edge (u, v)
    
props to: http://hetland.org/coding/python/bellman_ford.py
"""
from math import log
import requests
import json
from binance.client import Client

"""
headers= {'Accept': 'application/json', 'User-Agent': 'binance/python', 'X-MBX-APIKEY': '5ZskPFW3CeJEpbWItVTrPsy2ngSn3d1ued0cOH2kHipVuIhkMfETgxRN8Ljzrv9Q'}
tickers = requests.get("https://api.binance.com/api/v1/ticker/24hr", headers=headers)
"""

client = Client('5ZskPFW3CeJEpbWItVTrPsy2ngSn3d1ued0cOH2kHipVuIhkMfETgxRN8Ljzrv9Q', 'tCsChD24BHmLjqSVcYFgY1TzPKLji9OAzVlJdQlSPhL7t2O8PDwWFhrkbhVqyuvA')

def initialize(graph, source):
    d = {}
    p = {}
    for node in graph:
        d[node] = float('inf')
        p[node] = None
    d[source] = 0
    return d, p

def relax(u, v, graph, d, p):
    try:
        if d[v] > d[u] + graph[u][v]:
            try:
                d[v] = d[u] + graph[u][v]
                p[v] = u
            except:
                print('')
    except:
        print('')

def retrace_negative_loop(p, start):
    arbitrageLoop = [start]
    next_node = start
    while True:
        next_node = p[next_node]
        if next_node not in arbitrageLoop:
            arbitrageLoop.append(next_node)
        else:
            arbitrageLoop.append(next_node)
            arbitrageLoop = arbitrageLoop[arbitrageLoop.index(next_node):]
            return arbitrageLoop

def bellman_ford(graph, source):
    d, p = initialize(graph, source)
    start = None
    for i in range(len(graph)-1):
        for u in graph:
            for v in graph[u]:
                relax(u, v, graph, d, p)
    # one more relaxation to find negative weight cycle
    for u in graph:
        for v in graph[u]:
            try:
                if d[v] > d[u] + graph[u][v]:
                    #relax(u, v, graph, d, p)
                    start = u
                    return retrace_negative_loop(p, start)
                    #return d,p,start
            except:
                print('')
    #return d,p,start
    return None

def test():

    graph = {
        'ETH': {},
        'BTC': {},
        'EOS': {},
        'USDT': {},
        'XRP': {},
        'ETC': {},
        }
    
    """
    ETHBTC = client.get_ticker(symbol='ETHBTC')
    EOSETH = client.get_ticker(symbol='ETHBTC')
    EOSBTC = client.get_ticker(symbol='ETHBTC')
    EOSUSDT = client.get_ticker(symbol='ETHBTC')
    ETHUSDT = client.get_ticker(symbol='ETHBTC')
    XRPETH = client.get_ticker(symbol='ETHBTC')
    XRPBTC = client.get_ticker(symbol='ETHBTC')
    XRPUSDT = client.get_ticker(symbol='ETHBTC')
    ETCETH = client.get_ticker(symbol='ETHBTC')
    ETCBTC = client.get_ticker(symbol='ETHBTC')
    ETCUSDT = client.get_ticker(symbol='ETHBTC')
    """
    #ee = client.get_ticker(symbol='ETHBTCH')
    graph['ETH']['BTC'] = 12
    print(graph)
    for v in graph.keys():
        for u in graph.keys():
            symb = str(v) + str(u)
            try:
                ticker = client.get_ticker(symbol=v+u)
                try:
                    graph[v][u] = -log(float(ticker['bidPrice']))
                except  Exception as e:
                    print(str(e))
            except:
                graph[v][u] = None
        print('\n')

    #d, p, _ = bellman_ford(graph, 'a')
    res = bellman_ford(graph, 'ETH')
    print(res)
    """
    ETHBTC
    ETHEOS
    ETHUSDT
    ETHXRP
    ETHETC
    BTCETH
    BTCEOS
    BTCUSDT
    BTCXRP
    BTCETC
    EOSETH
    EOSBTC
    EOSUSDT
    EOSXRP
    EOSETC
    USDTETH
    USDTBTC
    USDTEOS
    USDTXRP
    USDTETC
    XRPETH
    XRPBTC
    XRPEOS
    XRPUSDT
    XRPETC
    ETCETH
    ETCBTC
    ETCEOS
    ETCUSDT
    ETCXRP

    | grep "EOSETH"
    g.add_vertex('eth')
    g.add_vertex('btc')
    g.add_vertex('eos')
    g.add_vertex('usdt')
    g.add_vertex('xrp')
    g.add_vertex('etc')
    assert d == {
        'a':  0,
        'b': -1,
        'c':  2,
        'd': -2,
        'e':  1
        }
    
    assert p == {
        'a': None,
        'b': 'a',
        'c': 'b',
        'd': 'e',
        'e': 'b'
        }
        """

if __name__ == '__main__':
    test()