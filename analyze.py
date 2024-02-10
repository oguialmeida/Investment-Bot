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
    csv_file_path = 'currency_data.csv'
    
    if os.path.exists(csv_file_path):
        existing_data = pd.read_csv(csv_file_path)
        last_date = existing_data['Date'].max()
    else:
        existing_data = pd.DataFrame(columns=['Coin', 'Date', 'Volume', 'High', 'Low'])
        last_date = start - pd.DateOffset(days=1)  # Inicializa a última data com um dia antes do início

    df_list = []

    for acronym in acronyms:
        try:
            data = yf.download(acronym.replace("USD", "-USD"), start=last_date, end=end)
            data['Coin'] = acronym
            data.reset_index(inplace=True)  # Resetando o índice para a data se tornar uma coluna
            data = data[['Coin', 'Date', 'Volume', 'High', 'Low']]
            df_list.append(data)
            print(f"Dados obtidos para {acronym}.")
        except Exception as e:
            print(f"Erro ao obter dados para {acronym}: {e}")

        time.sleep(1)

    if len(df_list) > 0:
        new_data = pd.concat(df_list)
        merged_data = pd.concat([existing_data, new_data])
        merged_data.to_csv(csv_file_path, index=False)
        return merged_data
    else:
        return existing_data
    
download_info_coin(datetime(2024, 2, 4), datetime.now().date().isoformat())
