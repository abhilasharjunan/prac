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

    return float(stock_fut['Settle Price'][0])

def get_list_of_futures_price_for_next_months(symbol):
    month={1:"JAN", 2:"FEB",3:"JAN",4:"JAN",5:"JAN",6:"JAN",7:"JUL",8:"AUG",9:"SEP",10:"OCT",11:"NOV",12:"DEC"};
    
    day_val = get_month_expiry_dates()
    val = get_symbol_futures_price(symbol,day_val[0],day_val[1],day_val[2])

    day_val_next_month = get_month_expiry_dates(1)
    val_next_month = get_symbol_futures_price('SBIN',day_val_next_month[0],day_val_next_month[1],day_val_next_month[2])

    print("Symbol : "+symbol)
    print("===================")
    print("closePrice : "+str(nse.get_quote(symbol)['closePrice']))
    print(month[day_val[1]] + " Fut Price : " + str(val))
    print(month[day_val_next_month[1]] + " Fut Price : " + str(val_next_month))
    print("********************")
