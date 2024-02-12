import os
import requests
import time
import yfinance as yf
import pandas as pd
import json
import constants
from datetime import datetime

# Datas para download
initial_date = datetime(2024, 2, 7)
final_date = datetime.now().date().isoformat()

# Checa a existência da moeda na plataforma
def check_coin_existence(coin_pair):
    endpoint = "/0/public/Ticker"
    pair_url = f"{constants.api_url_broker}{endpoint}?pair={coin_pair}"

    response = requests.get(pair_url).json()['error']

    if len(response) == 0:
        return True
    else:
        return False

# Retorna uma lista com as moedas da plataforma
def existing_coins():
    json_file_path = './data/coins.json'
    
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

# Faz o download das informações que irão se manipuladas
def download_info_coin(start, end):
    acronyms = existing_coins()
    csv_file_path = './data/currency_data.csv'
    
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

# Calcula a variação histórica da moeda e adiciona pesos de segurança
def calc_history_variation(today_price, yesterday_price, week_price, year_price):   
    variation_total = ((today_price - yesterday_price) * 2) + ((today_price - week_price) * 2.5) + ((today_price - year_price) * 3)
    return variation_total

# Escolhe a moeda com melhor crescimento
def chose_best_growth():
    return

# Usa tecnicas de deep learning para prever o crescimento da moeda
def coin_predict():
    return

# Analisa as melhores moedas de acordo com sites de notícias
def check_coin_news():
    return

# Realiza a analise de risco de se manter a moeda
def check_risk():
    return
