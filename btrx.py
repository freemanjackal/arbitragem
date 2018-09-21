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
import threading

"""
headers= {'Accept': 'application/json', 'User-Agent': 'binance/python', 'X-MBX-APIKEY': '5ZskPFW3CeJEpbWItVTrPsy2ngSn3d1ued0cOH2kHipVuIhkMfETgxRN8Ljzrv9Q'}
tickers = requests.get("https://api.binance.com/api/v1/ticker/24hr", headers=headers)
"""


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
                pass
    except:
        pass

def retrace_negative_loop(p, start, d):
    arbitrageLoop = [start]
    arbitragePrices = [d[start]]
    next_node = start
    try:
        while True:
            next_node = p[next_node]
            if next_node not in arbitrageLoop:
                arbitrageLoop.append(next_node)
                arbitragePrices.append(d[next_node])
            else:
                arbitrageLoop.append(next_node)
                arbitrageLoop = arbitrageLoop[arbitrageLoop.index(next_node):]
                return arbitrageLoop, arbitragePrices
    except Exception as e:
        #print(e)
        return None, None

def bellman_ford(graph, source):
    d, p = initialize(graph, source)
    start = None

    for i in range(len(graph)-1):
        for u in graph:
            for v in graph[u]:
                relax(u, v, graph, d, p)
    # one more relaxation to find negative weight cycle
    print('ass')
    for u in graph:
        for v in graph[u]:
            print("last relax")
            try:
                if d[v] > d[u] + graph[u][v]:
                    #relax(u, v, graph, d, p)
                    start = u
                    print('startttttttttttt ' + start)
                    return retrace_negative_loop(p, start, d)
                    #return d,p,start
            except Exception as e:
                pass
    #return d,p,start
    return None, None

def test():
    threading.Timer(50.0, test).start()

    graph = {
        'ETH': {},
        'BTC': {},
        'XRP': {},
        }
    graphOriginal = {
        'ETH': {},
        'BTC': {},
        'XRP': {},
        }
    
     
    for v in graph.keys():
        for u in graph.keys():
            try:
                payload = {'market': v+"-"+u}
                ticker = requests.get("https://bittrex.com/api/v1.1/public/getticker/", params=payload).json()
                try:
                    
                        graph[v][u] = -log(float(ticker['result']['Bid']))
                        graphOriginal[v][u] = float(ticker['result']['Bid'])
                        graph[u][v] = -log(1/float(ticker['result']['Ask']))
                        graphOriginal[u][v] = 1/float(ticker['result']['Ask'])


                except  Exception as e:
                    pass
            except:
                pass

    #print(graphOriginal)
                #graph[v][u] = None
    #d, p, _ = bellman_ford(graph, 'a')
    res, pre = bellman_ford(graph, 'ETH')

    value = 1
    valueO = value
    if res != None:
        for i in range(len(res), 1, -1):
            pre = graphOriginal[res[i-1]][res[i-2]]
            print(str(res[i-1])+str(res[i-2]))
            value *= pre
            #print("before fee--" + str(value))
            value = value - value/100*0.25
            #print("after fee--" + str(value))
            #print(value)

    print("gains " + str(value - valueO))
    if (value - valueO) > 0:
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")


if __name__ == '__main__':
     test()
