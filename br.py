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
from pydub import AudioSegment
from pydub.playback import play



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
        'eth': {},
        'btc': {},
        'brl': {},
        'xrp': {},
        }
    graphOriginal = {
        'eth': {},
        'btc': {},
        'brl': {},
        'xrp': {},
        }
    

     
    for v in graph.keys():
        for u in graph.keys():
            symb = str(v) + str(u)
            try:
                ticker = requests.get("https://braziliex.com/api/v1/public/ticker/" + v+"_"+u).json()
                try:
                    
                        graph[v][u] = -log(float(ticker['highestBid']))
                        graphOriginal[v][u] = float(ticker['highestBid'])
                        graph[u][v] = -log(1/float(ticker['lowestAsk']))
                        
                        graphOriginal[u][v] = 1/float(ticker['lowestAsk'])
                        


                except  Exception as e:
                    pass
            except:
                pass

                    #graph[v][u] = None
    #d, p, _ = bellman_ford(graph, 'a')
    res, preco = bellman_ford(graph, 'eth')

    value = 1
    valueO = value
    if res != None:
        for i in range(len(res), 1, -1):
            pre = graphOriginal[res[i-1]][res[i-2]]
            print(str(res[i-1])+str(res[i-2]))
            print('value  ' + str(value))
            print('pre  ' + str(pre))
            value *= pre
            #print('value*=pre  ' + str(value))
            #print("before fee--" + str(value))
            value = value - value/100*0.4999
            #print("after fee--" + str(value))
            print('value after fee' + str(value))

    print("gains " + str(value - valueO))
    if (value - valueO) > 0:
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        song = AudioSegment.from_mp3("alien.mp3")
        play(song)
        print(graphOriginal)


if __name__ == '__main__':
     test()
