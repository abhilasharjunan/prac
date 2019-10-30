#script to get all options 

#reference : https://www.capitalzone.in/category/automation/
from datetime import date
from datetime import datetime
import calendar
import requests
from nsetools import Nse
nse=Nse()
from bs4 import BeautifulSoup
from pprint import pprint
import json

PUTS=1
CALLS=2

return_string=""


def get_quote(sym):

	Base_url = "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol="+sym
	#print(Base_url)
	#print("before req" + str(datetime.now()))
	page = requests.get(Base_url)
	#print("After req" + str(datetime.now()))
	soup = BeautifulSoup(page.content, 'html.parser')
	#print("after converting" + str(datetime.now()))
	#print(soup)
	table_cls_2 = soup.find(id="responseDiv")
	quote=float(json.loads(table_cls_2.contents[0])['data'][0]['closePrice'].replace(",",""))
	return quote

def get_next_expiry_dates(monthly):
    month={1:"JAN", 2:"JAN",3:"JAN",4:"JAN",5:"JAN",6:"JAN",7:"JUL",8:"AUG",9:"SEP",10:"OCT",11:"NOV",12:"DEC"};
    year = datetime.now().year
    c = calendar.TextCalendar(calendar.THURSDAY)
    m = datetime.now().month
    val=""
    for i in c.itermonthdays(year,m):
        if i != 0 and datetime.now().day <= i:  #calendar constructs months with leading zeros (days belongng to the previous month)
            day = date(year,m,i)
            
            if day.weekday() == 3: #Thursday
                val=str(i)
                if(i<10):
                    val="0"+str
                val += str(month[m])+str(year)
                if monthly != 1:
                    return val
    return val

def print_resistence(entry):
    global return_string
    levels=[]
    oi_info={}
    oi_value=0
    for i in sorted(entry.keys()):
        levels.append(entry[i])
        oi_info[entry[i]]=i
        
    levels=levels[::-1]
    levels=levels[0:2]
    levels.sort()
    levels=levels[::-1]
    count=2
    ret=""
    R=[]
    for i in levels:
        val="Resistence R" + str(count) + " : " + str(i) #+ "        OI : " + str(oi_info[i])
        R.append("R"+str(count)+" : "+str(i))
        oi_value += oi_info[i]
        count -= 1;
        print(val,end = "\n")
        return_string = return_string + val + "\n"
    return oi_value, R

def print_support(entry):
    global return_string
    levels=[]
    oi_info={}
    oi_value=0
    for i in sorted(entry.keys()):
        levels.append(entry[i])
        oi_info[entry[i]]=i
    levels=levels[::-1]
    levels=levels[0:2]
    levels.sort()
    levels=levels[::-1]
    count=1
    S=[]
    for i in levels[0:2]:
        val="Support S" + str(count) + " : " + str(i) #+ "           OI : " + str(oi_info[i])
        S.append("S"+str(count)+" : "+str(i))
        oi_value += oi_info[i]
        count += 1;
        print(val,end = "\n")
        return_string=return_string + val + "\n"
    return oi_value, S

def get_options_chain_data(symbol,expdate):

    Base_url = "https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbol=" + symbol + "&date=" + expdate

    page = requests.get(Base_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    print("Got option chain response from nse")
    table_cls_2 = soup.find(id="octable")
    req_row = table_cls_2.find_all('tr')
    return req_row

def extract_oi_data(req_row,calls_or_puts,current_index):
    count=0
    entries={}
    puts_list=[]
        
    for row_number, tr_nos in enumerate(req_row):

		# This ensures that we use only the rows with values
        if row_number <= 1 or row_number == len(req_row) - 1:
            continue
        td_columns = tr_nos.find_all('td')
        strike_price = int(float(BeautifulSoup(str(td_columns[11]), 'html.parser').get_text()))
        if(calls_or_puts == PUTS):
            oi=(BeautifulSoup(str(td_columns[21]), 'html.parser').get_text())
            
            if oi == "-":
                continue

            if strike_price > current_index:
                puts_list.reverse()
                for entry in puts_list:                    
                    l=entry.split(':')
                    entries[int(l[0])]= int(l[1])
                    count += 1
                    if count > 15:
                        break
                break
                
            oi=int(oi.strip().replace(',',''))
            puts_list.append(str(oi)+":"+str(strike_price))
            
        else:
            oi=(BeautifulSoup(str(td_columns[1]), 'html.parser').get_text())
            
            if oi == "-" or strike_price < current_index:
                continue
            count = count + 1
            
            if count > 15:
                break
            oi=int(oi.strip().replace(',',''))
            entries[oi]= strike_price
    return entries
		    
	
def get_RAndS_levels(symbol):
    global return_string
    index=0
    
    if(len(symbol) == 0):
        index=1
        
    if(index):
        symbol="BANKNIFTY"
        expdate=get_next_expiry_dates(0)
    else:
        expdate=get_next_expiry_dates(1)
        
    symbol_new="NIFTY BANK"
    current_index=0
    

    
    print("Resistence and Support: " + symbol.upper())
    print("Expiry Date: " + expdate)
    print("==================================================")
    if(index):
        current_index=nse.get_index_quote(symbol_new)['lastPrice']
    else:
        current_index=get_quote(symbol)
	
    print("got index quote:"+ str(datetime.now()))
    req_row = get_options_chain_data(symbol,expdate)
    print("got option chain data:"+ str(datetime.now()))
    calls=extract_oi_data(req_row,CALLS,current_index)
    print("got calls : "+ str(datetime.now()))
    puts=extract_oi_data(req_row,PUTS,current_index)
    print("got puts : " + str(datetime.now()))
	
    return_string=""
    return_string="Resistence and Support: " + symbol.upper() + "\n"
    return_string=return_string + "Expiry Date: " + expdate + "\n"
    return_string=return_string + "======================================" + "\n"

    c_oi,R=print_resistence(calls)
	
    return_string=return_string + "\n"
    print("",end = "\n")
	
    return_string=return_string + "Index Value:" + str(current_index) + "\n"
    print("Index Value : ",current_index)
    R.append("Index : " + str(current_index))
    return_string=return_string + "\n"
    print("",end = "\n")
	
    p_oi,S=print_support(puts)
	
    return_string=return_string + "\n"
    print("",end = "\n")
    R = R + S
    d={}
    d[symbol]=R
    if p_oi < c_oi:
        return_string=return_string + "Trend Negative" + "\n"
        print("Trend Negative")
        d[symbol].append("Trend Negative")
    else:
        return_string=return_string + "Trend Positive" + "\n"
        print("Trend Positive")
        d[symbol].append("Trend Positive")
    return_string = return_string + "*************************************************\n"
    print("*************************************************")
    return return_string,d

consolidated={}
#get_RAndS_levels('')
stocks_list=['','HDFC','HDFCBANK','ICICIBANK','RELIANCE','INFY', 'MARUTI', 'TCS', 'BAJFINANCE']
for stock in stocks_list:
    s,d = get_RAndS_levels(stock)
    if stock == '':
        stock='BANKNIFTY'
    consolidated[stock]=d[stock]
print(json.dumps(consolidated, indent = 4))
