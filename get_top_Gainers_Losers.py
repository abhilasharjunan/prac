from nsetools import Nse;
from datetime import datetime;
nse = Nse();



print("Timestamp : ", datetime.now())

#print("Trading stratergy: In 5- min candle check if any of the five stocks have higher highs and lower lows");
top_gainers = nse.get_top_gainers();
top_losers = nse.get_top_losers();

print("=============")
print("Top Gainers");
print("=============")
for i in range(0,5):
    print(top_gainers[i]['symbol']);
print("=============")
print("Top Losers");
print("=============")
for i in range(0,5):
    print(top_losers[i]['symbol']);

fno_top_gainers = nse.get_top_fno_gainers();
fno_top_losers = nse.get_top_fno_losers();
print("=============")
print("Top FNO Gainers");
print("=============")
for i in range(0,5):
    print(fno_top_gainers[i]['symbol']);
print("=============")
print("Top FNO Losers");
print("=============")
for i in range(0,5):
    print(fno_top_losers[i]['symbol']);

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++");

print("Trading stratergy: Pre-Open Nifty");
    
nifty_printOpen = nse.get_preopen_nifty();

print("=============")
print("Nifty Pre-Open");
print("=============")
stock_map={}
for i in nifty_printOpen:
    stock_map[i['iVal']] = i['symbol'];    

val=0;    
for key,value in sorted(stock_map.items(),reverse=True):
    if(val == 5):
        break;
    
    print(value,key);
    val=val+1;

print()
print("Trading stratergy: Pre-Open FNO");
    
fno_printOpen = nse.get_preopen_fno();

print("=============")
print("FNO Pre-Open");
print("=============")

stock_map={}

for i in fno_printOpen:
    stock_map[i['iVal']] = i['symbol'];

val=0;    
for key,value in sorted(stock_map.items(),reverse=True):
    if(val == 5):
        break;
    
    print(value,key);
    val=val+1;
