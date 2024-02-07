import requests
import time
import yfinance as yf
import pandas as pd
from datetime import datetime

def calc_variation(today_price, yesterday_price, week_price, year_price):   
    variation_total = ((today_price - yesterday_price) * 2) + ((today_price - week_price) * 2.5) + ((today_price - year_price) * 3)
    
    return variation_total

def check_coin_existence(coin_pair):
    api_url_kraken = "https://api.kraken.com"
    endpoint = "/0/public/Ticker"
    pair_url = f"{api_url_kraken}{endpoint}?pair={coin_pair}"

    response = requests.get(pair_url).json()['error']

    if len(response) == 0:
        return True
    else:
        return False

def check_coins():
    acronyms = ['BTCUSD', 'ETHUSD', 'USDTUSD', 'SOLUSD', 'XRPUSD', 'USDCUSD', 'ADAUSD', 'AVAXUSD', 'DOGEUSD', 'LINKUSD', 'TRXUSD', 'DOTUSD', 'MATICUSD', 'ICPUSD', 'DAIUSD', 'SHIBUSD', 'LTCUSD', 'BCHUSD', 'ETCUSD', 'UNIUSD', 'ATOMUSD', 'XLMUSD', 'XMRUSD', 'APTUSD', 'OPUSD', 'IMXUSD', 'INJUSD', 'NEARUSD', 'TIAUSD', 'FILUSD', 'LDOUSD', 'ARBUSD', 'STXUSD', 'MKRUSD', 'RNDRUSD', 'SUIUSD', 'TUSDUSD', 'RUNEUSD', 'SEIUSD', 'GRTUSD', 'EGLDUSD', 'ALGOUSD', 'AAVEUSD', 'MINAUSD', 'QNTUSD', 'FLOWUSD', 'FLRUSD', 'ASTRUSD', 'FTMUSD', 'SANDUSD', 'AXSUSD', 'SNXUSD', 'XTZUSD', 'CHZUSD', 'MANAUSD', 'EOSUSD', 'BTTUSD', 'FXSUSD', 'KAVAUSD', 'BLURUSD', 'PYTHUSD', 'JUPUSD', 'CTSIUSD', 'BANDUSD', 'CHZUSD', 'AUDIOUSD', 'XTZUSD', 'ALPHAUSD', 'NMRUSD', 'MIRUSD', 'BLZUSD', 'LPTUSD', 'AGLDUSD', 'FLOWUSD', 'KSMUSD', 'NANOUSD', 'EWTUSD', 'ARPAUSD', 'ZRXUSD', 'REQUSD', 'CRVUSD', 'SANDUSD', 'PHAUSD', 'UNFIUSD', 'TVKUSD', 'ENSUSD', 'OGNUSD', 'CELRUSD', 'DENTUSD', 'QNTUSD', 'FETUSD', 'UMAUSD', 'BANDUSD', 'WOOUSD']
    size_arr = len(acronyms)
    
    exist_coin = []
    count = 0

    # Garante que existe a moeda na API
    for acronyms in acronyms:
        if check_coin_existence(acronyms):
            exist_coin.append(acronyms)
            count += 1
            print(f"Existe: {acronyms}... {str(count)} de {size_arr}")
        time.sleep(1)

    return exist_coin

def get_coin_value():
    start = datetime(2020, 1, 1)
    end = datetime.now().date().isoformat()
    symbol = 'BTC-USD'
    
    df = yf.download(symbol, start=start, end=end)
    
    print(df)

def chose_coin():
    valid_coins = check_coins()

    print(valid_coins)
    
get_coin_value()

