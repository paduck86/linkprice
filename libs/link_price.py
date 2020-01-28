import time
import requests
import datetime
from configs import base as cfg

class LinkPrice(object):
    def __init__(self):
        self.UPBIT_TICKER_API_URL = cfg.UPBIT_TICKER_API_URL
        self.BINANCE_TICKER_API_URL = cfg.BINANCE_TICKER_API_URL
        self.EXCHANGE_RATE_API_URL = cfg.EXCHANGE_RATE_API_URL
        self.BITBOX_API_KEY = cfg.BITBOX_API_KEY
        self.BITBOX_TICKER_API_URL = cfg.BITBOX_TICKER_API_URL
        self.BITBOX_ORDERBOOKS_API_URL = cfg.BITBOX_ORDERBOOKS_API_URL
        self.BITBOX_HISTORY_API_URL = cfg.BITBOX_HISTORY_API_URL
        self.BITBOX_LINK_BTC_COINPAIR = 'LINK.BTC'

    def format_percent(self, percent):
        if str(percent)[:1] not in ('+','-'):
            percent = '+' + str(percent)
        else:
            percent = str(percent)
        return percent

    def get_upbit_price(self):
        def get_upbit_data(market):
            url = self.UPBIT_TICKER_API_URL
            querystring = {"markets": market}
            response = requests.request("GET", url, params=querystring)
            price = response.json()[0]['trade_price']
            return price
        btc_krw = get_upbit_data('KRW-BTC')
        btc_krw = int(btc_krw)
        btc_usdt = get_upbit_data('USDT-Btc')
        btc_usdt = round(btc_usdt,2)
        return btc_krw, btc_usdt

    def get_binance_price(self, coin_pair='BTCUSDT'):
        url = self.BINANCE_TICKER_API_URL + '?symbol={}'.format(coin_pair)
        response = requests.request("GET", url)
        binance_price = response.json()['price']
        return binance_price

    def get_exchange_rate(self, currency_pair='USDKRW'):
        url = self.EXCHANGE_RATE_API_URL + '{}'.format(currency_pair)
        response = requests.request("GET", url)
        exchange_rate = response.json()[currency_pair][0]
        return exchange_rate

    def get_link_price(self):
        url = self.BITBOX_TICKER_API_URL + "?coinPair={}".format(self.BITBOX_LINK_BTC_COINPAIR)
        response = requests.get(url, headers={"X-API-Key": self.BITBOX_API_KEY})
        result = response.json()
        btc_price = result['responseData']['last']
        btc_volume = result['responseData']['volume']

        return btc_price, btc_volume

    def get_link_orderbooks(self):
        url = self.BITBOX_ORDERBOOKS_API_URL + "?coinPair={}&depth=10".format(self.BITBOX_LINK_BTC_COINPAIR)
        response = requests.get(url, headers={"X-API-Key": self.BITBOX_API_KEY})
        result = response.json()
        ask = result['responseData']['ASK']
        bid = result['responseData']['BID']

        orderbook_txt = '[ASK]\n'
        for idx in range(len(ask)):
            price = ask[idx]['price']
            amount = ask[idx]['amount']
            if len(str(price)) < 10:
                price = str(price) + '0' * (10 - len(str(price)))
            txt = str(price) + '     ' + str(amount)
            orderbook_txt = orderbook_txt + txt + '\n'

        orderbook_txt = orderbook_txt + '\n[BID]\n'
        for idx in range(len(bid)):
            price = bid[idx]['price']
            amount = bid[idx]['amount']
            if len(str(price)) < 10:
                price = str(price) + '0' * (10 - len(str(price)))
            txt = str(price) + '     ' + str(amount)
            orderbook_txt = orderbook_txt + txt + '\n'

        return orderbook_txt

    def get_link_trade_history(self):
        url = self.BITBOX_HISTORY_API_URL + "?coinPair={}&max=10".format(self.BITBOX_LINK_BTC_COINPAIR)
        response = requests.get(url, headers={"X-API-Key": self.BITBOX_API_KEY})
        result = response.json()
        result_data = result['responseData']

        hist_txt ='[TRADE_HISTORY]\n'
        for i, hist in enumerate(result_data):
            price = str(hist['price'])
            created_at = hist['createdAt']
            tz = datetime.timezone(datetime.timedelta(hours=9))
            created_date = datetime.datetime.fromtimestamp(int(created_at)/1000, tz)
            create_datestr = '{}-{}-{} {}:{}:{}'.format(created_date.year, str(created_date.month).rjust(2, '0'), str(created_date.day).rjust(2, '0'), str(created_date.hour).rjust(2, '0'), str(created_date.minute).rjust(2, '0'), str(created_date.second).rjust(2, '0'))
            if hist['orderSide'] == 'SELL':
                hist_txt = hist_txt + "(-) SELL ::   " + str(hist['price']).ljust(10, '0') + "     " + str(hist['amount']) + '\n'
            else:
                hist_txt = hist_txt + "(+) BUY ::   " + str(hist['price']).ljust(10, '0') + "     " + str(hist['amount']) + '\n'
            hist_txt = hist_txt + create_datestr.rjust(25) + '\n'
        return hist_txt
