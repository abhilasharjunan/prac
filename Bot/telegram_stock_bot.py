import requests
import json
import configparser as cfg

class telegram_stock_bot():
	def __init__(self, config):
		self.token="1042935124:AAEyWEDrlIM6Uhki8ZpOBNItIHmpver0Mgw"
		self.base = "https://api.telegram.org/bot{}".format(self.token)
	
	def get_updates(self, offset=None):
		
		url = self.base + "/getUpdates?timeout=5"
		
		if offset:
		    url = url + "&offset={}".format(offset+1)
        
		try:
			r = requests.get(url)
		except:
			return {}
			
		return json.loads(r.content)
		
	def send_message(self, message, chat_id):
		url = self.base + "/sendMessage?chat_id={}&text={}".format(chat_id,message)
		if message is not None:
		    requests.get(url)
			
	def read_from_config_file(self, config):
		parser = cfg.ConfigParser()
		parser.read(config)
		return parser.get('creds','token')

