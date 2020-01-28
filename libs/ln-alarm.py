import telegram
from configs import base as cfg
from libs.link_price import LinkPrice

TELEGRAM_TOKEN = cfg.TELEGRAM_TOKEN
TELEGRAM_CHAT_ID = cfg.TELEGRAM_CHAT_ID
BOT = telegram.Bot(token=TELEGRAM_TOKEN)
link_price = LinkPrice()

if __name__ == '__main__':
    upbit_btc_krw, upbit_btc_usdt = link_price.get_upbit_price()
    binance_btc_usdt = link_price.get_binance_price()
    exchange_rate = link_price.get_exchange_rate()
    btc_ln_price, btc_ln_volume = link_price.get_link_price()
    orderbooks = link_price.get_link_orderbooks()

    history = link_price.get_link_trade_history()

    upbit_ln_krw = round(upbit_btc_krw * btc_ln_price, 2)
    upbit_ln_usdt = round(upbit_ln_krw / exchange_rate, 2)

    upbit_btc_usdt = round(upbit_btc_krw / exchange_rate, 2)

    binance_btc_krw = int(float(binance_btc_usdt) * exchange_rate)
    binance_btc_usdt = round(float(binance_btc_usdt), 2)

    btc_ln_volume = round(btc_ln_volume, 2)

    korea_premium = round(((upbit_btc_krw - binance_btc_krw) / binance_btc_krw) * 100, 2)

    price_text = '{} | {:,}￦ ({}$)\nUpbit LN conv : {:,}￦ ({}$)\nLN\BTC            : {} (vol. {}) \n'.format(btc_ln_price, upbit_ln_krw, upbit_ln_usdt, upbit_ln_krw, upbit_ln_usdt, btc_ln_price, btc_ln_volume)
    price_text += 'Upbit BTC      : {:,}￦ ({}$)\n'.format(upbit_btc_krw, upbit_btc_usdt)
    price_text += 'Binance BTC : {:,}￦ ({}$)\n'.format(binance_btc_krw, binance_btc_usdt)
    price_text += 'Korea Premium : {}%\n'.format(korea_premium)
    price_text += 'Exchange Rate : {}￦'.format(exchange_rate)

    BOT.sendMessage(chat_id=TELEGRAM_CHAT_ID, text=history, parse_mode='HTML')
    BOT.sendMessage(chat_id=TELEGRAM_CHAT_ID, text=orderbooks, parse_mode='HTML')
    BOT.sendMessage(chat_id=TELEGRAM_CHAT_ID, text=price_text, parse_mode='HTML')

