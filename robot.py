from binance.um_futures import UMFutures
from tradingview_ta import TA_Handler, Interval, Exchange
import time
import requests

INTERVAL = Interval.INTERVAL_4_HOURS
TELEGRAM_TOKEN = '6161966809:AAFHPm1QsHieaRjWzyIpive4tIrWOEF-fIY'
TELEGRAM_CHANNEL = '@signalsleopold'

client = UMFutures()


def get_data(symbol):
    output = TA_Handler(symbol=symbol,
                        screener='Crypto',
                        exchange='Binance',
                        interval= INTERVAL)
    
    activiti = output.get_analysis().summary
    activiti['SYMBOL'] = symbol
    return activiti

def get_symbols():
    tickers = client.mark_price()
    symbols = []
    for i in tickers:
        ticker = i['symbol']
        symbols.append(ticker)
    return symbols

def send_message(text):
    res = requests.get('https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN), params=dict(
    chat_id=TELEGRAM_CHANNEL, text=text))


symbols = get_symbols()
longs = []
shorts = []

def first_data():
    print('Searching First Data')
    send_message('Поиск первичных сигналов...')
    for i in symbols:
            try:
                data = get_data(i)
                if (data['RECOMMENDATION'] == 'STRONG_BUY'):
                     longs.append(data['SYMBOL'])

                if (data['RECOMMENDATION'] == 'STRONG_SELL'):
                        shorts.append(data['SYMBOL'])
                time.sleep(0.01)
            except:
                  pass


    print('longs:')
    print(longs)
    print('shorts:')
    print(shorts)
    return longs, shorts

print('Start')
send_message('Поехали!')
first_data()


while True:
    print('_______________!!!Жду новые сигналы!!!________________')
    for i in symbols:
        try:
            data = get_data(i)
            if (data['RECOMMENDATION'] == 'STRONG_BUY' and (data['SYMBOL'] not in longs)):
                 print(data['SYMBOL'], 'Buy')
                 text = data['SYMBOL'] + ' BUY'
                 send_message(text)
                 longs.append(data['SYMBOL'])



            if (data['RECOMMENDATION'] == 'STRONG_SELL' and (data['SYMBOL'] not in shorts)):
                 print(data['SYMBOL'], 'Sell')
                 text = data['SYMBOL'] + ' SELL'
                 send_message(text)
                 shorts.append(data['SYMBOL'])
            time.sleep(0.1)
        except:
            pass
