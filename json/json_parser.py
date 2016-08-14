import json as js;
from pprint import pprint;
with open("network.json") as data_file:
    data = js.load(data_file)
L=[]
for i in data["graph"]["edges"]:
    print("Source : " + i["source"] + "-> Target : " + i["target"])
    L.append((i["source"],i["target"]))
	
print(L)