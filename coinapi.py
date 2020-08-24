import requests
import json
import telepot
from time import sleep
import logging


class Ticker:
	def __init__(self):
		self.chat_id = "INSERT_CHAT_ID_HERE"
		self.telegram_token = "INSERT_TELEGRAM_TOKEN_HERE"
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

		except Exception:
			sleep(30)
			self.get_coins_value()

	def telegram_poster(self):
		try:
			self.get_coins_value()

			bot = telepot.Bot(self.telegram_token)
			bot.sendMessage(chat_id=self.chat_id, text=f'\n{self.data}', parse_mode='Markdown')
			print("Message sent!")

		except Exception as e:
			logging.info(f"**** {e}")


def main():
	try:
		while True:
			d = Ticker()
			d.telegram_poster()
			sleep(5)

	except Exception:
		print("Exception in main")


if __name__ == '__main__':
	logging.basicConfig(
		level=logging.INFO,
		format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
		datefmt='%d-%m-%Y %H:%M:%S'
	)

	main()
