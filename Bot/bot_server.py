from telegram_stock_bot import telegram_stock_bot
from datetime import date
from nsepy import get_history
from nsepy.derivatives import get_expiry_date
from get_option_Rs_Ss import get_RAndS_levels

update_id = None
query_list = {}

bot = telegram_stock_bot("tele_bot.cfg")

def usage():
    return "\nUsage: Enter symbol to get Resistance and Support Levels\n Format For Stocks: stock:<symbol> Eg: stock:Infy\n Format For Bank Index: stock:BankNifty\n"

	
def check_query(msg):
	if '/help' in msg:
		return usage()
	elif '/start' in msg:
		return str("Welcome to Glyder's Runway Bot")
	elif 'stock:' in msg:
		return "success"
	else:
		return str("Command not Supported\n") + usage()
		
def make_reply(msg):
	if msg is not None:
		ret = check_query(msg)
		if 'success' in ret:
			# Stock options (Similarly for index options, set index = True)
			index=0
			stock=msg.split(":")[1].lower()
			if 'banknifty' in stock:
				index = 1
				#stock_fut = get_history(symbol=stock,start=date(2019,10,21),end=date(2019,10,25),index=True, futures=True,expiry_date=get_expiry_date(2019,10))
			else:
				index = 0
				#stock_fut = get_history(symbol=stock,start=date(2019,10,21),end=date(2019,10,25),futures=True,expiry_date=get_expiry_date(2019,10))
			#if stock_fut.empty:
				#return "Either Symbol:{} is invalid or is not in FNO List, Please try with valid Symbol Name".format(msg)

			print(stock)
			if index == 0:
				reply = get_RAndS_levels(stock)
			else:
				reply = get_RAndS_levels('')
		else:
			reply = ret

	return reply

while True:

	try:
		updates = bot.get_updates(offset=update_id)
		if updates == {}:
			continue
		print('Got request')
		updates = updates["result"]
		if updates:
			for item in updates:
				print('Checking update id ')
				update_id = item["update_id"]
				try:
					message = item["message"]["text"]
				except:
					message = None

				from_ =  item["message"]["from"]["id"]
				from_username = item["message"]["from"]["username"]
				print("Got message from " + from_username + " for stock:"+message)
				print('before Make replyd ')
				reply = make_reply(message)
				bot.send_message(reply, from_)
		#stopPoll
	except:
		continue
