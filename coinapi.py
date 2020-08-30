import requests
import json
import telepot
from time import sleep
import logging


class Ticker:
	def __init__(self):
		self.chat_id = "451960095"
		self.bot = telepot.Bot("1209375048:AAFNFz9_lnXaNmjR4W_zn1LCP4LF5t602-g")
		self.data = ''

	def get_coins_value(self):
		try:
			url = "https://dev-api.shrimpy.io/v1/exchanges/kucoin/ticker"
			r = requests.get(url)
			cont = r.json()

			coin_to_process = "BTC,ETH,XMR"  # Input coin to process here
			for item in coin_to_process.split(","):
				config_section = item.strip()
				if len(config_section) > 0:
					for conts in cont:
						if conts['symbol'] == config_section:
							name = conts['symbol']
							priceusd = round(float(conts['priceUsd']), 2)
							changes24h = round(float(conts['percentChange24hUsd']), 3)

							if "-" in str(changes24h):
								self.data += f'*{name}:* ${priceusd} ({changes24h}%) 💔\n'
							elif changes24h > 30:
								self.data += f'*{name}:* ${priceusd} ({changes24h}%) 🔔🔔🔔\n'
							else:
								self.data += f'*{name}:* ${priceusd} ({changes24h}%) ❤\n'

		except Exception as e:
			logging.info(f'{e}')
			sleep(30)
			self.get_coins_value()

	def telegram_poster(self):
		try:
			self.get_coins_value()
			self.bot.sendMessage(chat_id=self.chat_id, text=f'\n{self.data}', parse_mode='Markdown')
		except Exception as e:
			logging.info(f"**** {e}")

	def datatype_not_supported(self):
		self.bot.sendMessage(chat_id=self.chat_id, text=f'Other datatypes are not supported currently',
							 parse_mode='Markdown')

class TelegramListener(Ticker):
	def handle(self, msg):
		try:
			content_type, chat_type, chat_id = telepot.glance(msg)
			# print(f"{content_type}, {chat_type}, {chat_id}")

			if content_type == 'text' and msg["text"].lower() == "status":
				Ticker().telegram_poster()
				print("Message sent via request")
			elif content_type != 'text':
				Ticker().datatype_not_supported()

		except Exception as e:
			self.bot.sendMessage(self.chat_id, f"{e}")
			logging.info(f"Exception in handle: {e}")

	def telegram_listener_startup(self):
		self.bot.message_loop(self.handle)

def main():
	TelegramListener().telegram_listener_startup()
	print('Listening ...')

	try:
		while True:
			Ticker().telegram_poster()
			print("Message sent via loop")
			sleep(3600)

	except Exception as e:
		print(f"Exception in main: {e}")

if __name__ == '__main__':
	logging.basicConfig(
		level=logging.INFO,
		format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
		datefmt='%d-%m-%Y %H:%M:%S'
	)

	main()
