import time
import requests
import urllib.parse
import hashlib
import hmac
import base64
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

api_url_krakens = os.getenv("API_CORR")
api_url_awesome = os.getenv("API_REAL")
current_price = requests.get(f"{api_url_krakens}/0/public/Ticker?pair=BTCUSD").json()['result']['XXBTZUSD']['c'][0]
real_value = requests.get(f"{api_url_awesome}/json/last/USD-BRL").json()["USDBRL"]["high"]
api_key = os.getenv("API_KEY")
api_sec = os.getenv("API_SEC")
    
# Cria uma assinatura com base na chave
def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message  = urlpath.encode() + hashlib.sha256(encoded).digest()
    
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    
    return sigdigest.decode()

# Autentica e deixa pronta a url para ser usada com os endpoints
def kraken_request(url_path, data, api_key, api_sec):
    headers = {"API-Key": api_key, "API-Sign": get_kraken_signature(url_path, data, api_sec)}
    resp = requests.post((api_url_krakens + url_path), headers=headers, data=data)
    return resp

# Função que realiza a compra das crytos
def buying_currency(buy_amount):
    print(f"Buying {buy_amount} of BTC at {current_price}!")
    
    resp = kraken_request("/0/private/AddOrder", {
        "nonce": str(int(1000 * time.time())),
        "ordertype": "market",
        "type": "buy",
        "volume": buy_amount,
        "pair": "XBTUSD",
    }, api_key, api_sec)
    
    if not resp.json()['error']:
        print("Successfully bought BTC!")
    else:
        print(f"Error: { resp.json()['error'] }")

# Função que realiza a venda das cryptos      
def selling_currency(sell_amount):
    print(f"Selling {sell_amount} of BTC at {current_price}!")
    
    resp = kraken_request("/0/private/AddOrder", {
        "nonce": str(int(1000 * time.time())),
        "ordertype": "market",
        "type": "sell",
        "volume": sell_amount,
        "pair": "XBTUSD",
    }, api_key, api_sec)
    
    if not resp.json()['error']:
        print("Successfully sold BTC!")
    else:
        print(f"Error: { resp.json()['error'] }")
