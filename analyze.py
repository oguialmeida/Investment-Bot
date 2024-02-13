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
    with open(constants.json_data_path, 'r') as json_file:
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
def download_info_coin(start, end, csv_file_path):
    acronyms = existing_coins()
    
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

# Escolhe a moeda com melhor crescimento
def chose_best_growth(csv_file_path):
    # Leia o arquivo CSV
    data = pd.read_csv(csv_file_path)

    # Converte a coluna 'Date' para o tipo datetime
    data['Date'] = pd.to_datetime(data['Date'])

    # Calcula o percentual de crescimento histórico para cada moeda
    data['Growth'] = (data.groupby('Coin')['High'].transform('last') - data.groupby('Coin')['High'].transform('first')) / data.groupby('Coin')['High'].transform('first') * 100

    # Seleciona a moeda com o maior percentual de crescimento histórico
    best_coin = data.loc[data.groupby('Coin')['Growth'].idxmax(), 'Coin'].iloc[0]
    
    return best_coin

# Calcula a variação histórica da moeda e adiciona pesos de segurança
def calc_history_variation(today_price, yesterday_price, week_price, month_price, year_price):   
    variation_total = ((today_price - yesterday_price) * 2) + ((today_price - week_price) * 2.5) + ((today_price - month_price) * 3) + ((today_price - year_price) * 3.5)
    return variation_total

# Usa tecnicas de deep learning para prever o crescimento da moeda
def coin_predict():
    return

# Realiza a analise de risco de se manter a moeda
def check_risk(initial_amount, atual_amount):
    return
