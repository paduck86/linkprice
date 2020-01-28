# -- coding: utf-8 --
import os
from configparser import ConfigParser
import traceback

config_parser = ConfigParser()
config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config')
config_parser.read(config_file)

try:
    TELEGRAM_CHAT_ID = config_parser.get('config', 'TELEGRAM_CHAT_ID') or ''
    TELEGRAM_TOKEN = config_parser.get('config', 'TELEGRAM_TOKEN') or ''
    BITBOX_API_KEY = config_parser.get('config', 'BITBOX_API_KEY') or ''
except Exception as err:
    print(str(err))
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
    BITBOX_API_KEY = os.environ.get('BITBOX_API_KEY', '')

UPBIT_TICKER_API_URL = os.environ.get('UPBIT_TICKER_API_URL', 'https://api.upbit.com/v1/ticker')
BINANCE_TICKER_API_URL = os.environ.get('BINANCE_TICKER_API_URL', 'https://api.binance.com/api/v3/ticker/price')
EXCHANGE_RATE_API_URL = os.environ.get('EXCHANGE_RATE_API_URL', 'https://earthquake.kr:23490/query/')
BITBOX_TICKER_API_URL = os.environ.get('BITBOX_TICKER_API_URL', 'https://openapi.bitbox.me/v1/market/public/currentTickValue')
BITBOX_ORDERBOOKS_API_URL = os.environ.get('BITBOX_ORDERBOOKS_API_URL', 'https://openapi.bitbox.me/v1/market/public/orderBooks')
BITBOX_HISTORY_API_URL = os.environ.get('BITBOX_HISTORY_API_URL', 'https://openapi.bitbox.me/v1/market/public/tradeHistory')
