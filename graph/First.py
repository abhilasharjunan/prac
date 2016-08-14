import networkx as nx;

G=nx.Graph()
'''e=[('a','b',0.3),('b','c',0.9),('a','c',0.5),('c','d',1.2)]
#G.add_weighted_edges_from(e)
#print(nx.dijkstra_path(G,'a','d'))
'''
G.add_edge('A','B')
G.add_edge('B','C')
print(G.adj)
val = G.adj
print(val.keys())
print(val.values())