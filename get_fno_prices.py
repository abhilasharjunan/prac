from datetime import date
from datetime import datetime
import calendar
import requests
from nsetools import Nse
nse=Nse()
from nsepy import get_history
# Stock options (Similarly for index options, set index = True)

def get_month_expiry_dates(next_month=0):
    year = datetime.now().year
    c = calendar.TextCalendar(calendar.THURSDAY)
    m = datetime.now().month
    if next_month == 1:
        m += 1
        if m == 13:
            m=1
            year+=1
    val=[]
    for d in c.itermonthdays(year,m):
        if d != 0 and datetime.now().day <= d:  #calendar constructs months with leading zeros (days belongng to the previous month)
            day = date(year,m,d)
            if day.weekday() == 3: #Thursday
                 val = [d,m,year]
    return val

def get_symbol_futures_price(sym, day_val, mon_val, year_val):
    day=date(datetime.now().year,datetime.now().month,datetime.now().day)
    stock_fut = get_history(symbol=sym,
                        start=day,
                        end=day,
                        futures=True,
                        expiry_date=date(year_val,mon_val,day_val))
    
    return float(stock_fut['Last'][0])

def get_list_of_futures_price_for_next_months(symbol):
    month={1:"JAN", 2:"FEB",3:"JAN",4:"JAN",5:"JAN",6:"JAN",7:"JUL",8:"AUG",9:"SEP",10:"OCT",11:"NOV",12:"DEC"};
    
    lot_size = nse.get_fno_lot_sizes()[symbol]
        
    if lot_size < 1000 or lot_size > 10000:
        return
    
    day_val = get_month_expiry_dates()
    val = get_symbol_futures_price(symbol,day_val[0],day_val[1],day_val[2])

    day_val_next_month = get_month_expiry_dates(1)
    val_next_month = get_symbol_futures_price(symbol,day_val_next_month[0],day_val_next_month[1],day_val_next_month[2])
    
    spot_price = nse.get_quote(symbol)['closePrice']
    
    diff_with_spot_price_curr_month = spot_price - val
    if diff_with_spot_price_curr_month < 0:
        diff_with_spot_price_curr_month = val - spot_price
    
    diff_with_spot_price_next_month = spot_price - val_next_month
    if diff_with_spot_price_next_month < 0:
        diff_with_spot_price_next_month = val_next_month - spot_price
    
    if diff_with_spot_price_curr_month < 5:
        if diff_with_spot_price_next_month < 5:
            return

    diff = val - val_next_month
    
    if diff < 0:
        diff = val_next_month - val
    
    if(diff < 1):
        return
    
    print("Symbol : "+symbol + "   Lot Size : " + str(lot_size))
    print("===================")
    print("Stock Price : "+str(spot_price))
    print(month[day_val[1]] + " Fut Price : " + str(val))
    print(month[day_val_next_month[1]] + " Fut Price : " + str(val_next_month))
    print("********************")

fno_list = ['ACC','ADANIENT','ADANIPORTS','ADANIPOWER','AMARAJABAT','AMBUJACEM','APOLLOHOSP','APOLLOTYRE','ASHOKLEY',
            'ASIANPAINT','AUROPHARMA','AXISBANK','BAJAJ-AUTO','BAJAJFINSV','BAJFINANCE','BALKRISIND','BANKBARODA',
            'BANKINDIA','BATAINDIA','BEL','BERGEPAINT','BHARATFORG','BHARTIARTL','BHEL','BIOCON','BOSCHLTD','BPCL','BRITANNIA',
            'CADILAHC','CANBK','CASTROLIND','CENTURYTEX','CESC','CHOLAFIN','CIPLA','COALINDIA','COLPAL','CONCOR',
            'CUMMINSIND','DABUR','DISHTV','DIVISLAB','DLF','DRREDDY','EICHERMOT','EQUITAS','ESCORTS','EXIDEIND','FEDERALBNK',
            'GAIL','GLENMARK','GMRINFRA','GODREJCP','GRASIM','HAVELLS','HCLTECH','HDFC','HDFCBANK','HEROMOTOCO','HEXAWARE',
            'HINDALCO','HINDPETRO','HINDUNILVR','IBULHSGFIN','ICICIBANK','ICICIPRULI','IDEA','IDFCFIRSTB','IGL','INDIGO',
            'INDUSINDBK','INFRATEL','INFY','IOC','ITC','JINDALSTEL','JSWSTEEL','JUBLFOOD','JUSTDIAL','KOTAKBANK','L&TFH',
            'LICHSGFIN','LT','LUPIN','M&M','M&MFIN','MANAPPURAM','MARICO','MARUTI','MCDOWELL-N','MFSL','MGL','MINDTREE',
            'MOTHERSUMI','MRF','MUTHOOTFIN']
for symbol in fno_list:
    get_list_of_futures_price_for_next_months(symbol)
    
fno_list = ['NATIONALUM','NBCC','NCC','NESTLEIND','NIITTECH','NMDC','NTPC','OIL','ONGC',
            'PAGEIND','PEL','PETRONET','PFC','PIDILITIND','PNB','POWERGRID','PVR','RAMCOCEM','RBLBANK','RECLTD','RELIANCE',
            'SAIL','SBIN','SHREECEM','SIEMENS','SRF','SRTRANSFIN','STAR']{'SUNPHARMA','SUNTV','TATACHEM','TATAELXSI',
            'TATAGLOBAL','TATAMOTORS','TATAMTRDVR','TATAPOWER','TATASTEEL','TCS','TECHM','TITAN','TORNTPHARM','TORNTPOWER',
            'TVSMOTOR','UBL','UJJIVAN','ULTRACEMCO','UNIONBANK','UPL','VEDL','VOLTAS','WIPRO','YESBANK','ZEEL']
for symbol in fno_list:
    get_list_of_futures_price_for_next_months(symbol)
                                                                          
fno_list = ['SUNPHARMA','SUNTV','TATACHEM','TATAELXSI',
            'TATAGLOBAL','TATAMOTORS','TATAMTRDVR','TATAPOWER','TATASTEEL','TCS','TECHM','TITAN','TORNTPHARM','TORNTPOWER',
            'TVSMOTOR','UBL','UJJIVAN','ULTRACEMCO','UNIONBANK','UPL','VEDL','VOLTAS','WIPRO','YESBANK','ZEEL']
for symbol in fno_list:    
    get_list_of_futures_price_for_next_months(symbol)                                                                          
