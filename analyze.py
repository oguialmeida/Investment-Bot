import os
import requests
import time
import yfinance as yf
import pandas as pd
import json
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def calc_variation(today_price, yesterday_price, week_price, year_price):   
    variation_total = ((today_price - yesterday_price) * 2) + ((today_price - week_price) * 2.5) + ((today_price - year_price) * 3)
    
    return variation_total

def check_coin_existence(coin_pair):
    api_url_kraken = os.getenv("API_CORR")
    endpoint = "/0/public/Ticker"
    pair_url = f"{api_url_kraken}{endpoint}?pair={coin_pair}"

    response = requests.get(pair_url).json()['error']

    if len(response) == 0:
        return True
    else:
        return False

def check_coins():
    json_file_path = 'coins.json'
    
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
        acronyms = json_data['coins']
        
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

def download_info_coin(start, end):
    acronyms = check_coins()
    
    df_list = []

    for acronym in acronyms:
        try:
            data = yf.download(acronym.replace("USD", "-USD"), start=start, end=end)
            data['Coin'] = acronym
            df_list.append(data)
            print(f"Dados obtidos para {acronym}.")
        except Exception as e:
            print(f"Erro ao obter dados para {acronym}: {e}")

        time.sleep(1)

    if len(df_list) > 0:
        df = pd.concat(df_list)
        df.to_csv('currency_data.csv', index=False)
        return df
    else:
        return None
    
download_info_coin(datetime(2024, 2, 4), datetime.now().date().isoformat())
