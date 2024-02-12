import time
import requests
import broker_auth
import constants

current_price = requests.get(f"{constants.api_url_broker}/0/public/Ticker?pair=BTCUSD").json()['result']['XXBTZUSD']['c'][0]
real_value = requests.get(f"{constants.api_url_awesome}/json/last/USD-BRL").json()["USDBRL"]["high"]
    
# Função que realiza a compra das crytos
def buying_currency(buy_amount):
    print(f"Buying {buy_amount} of BTC at {current_price}!")
    
    resp = broker_auth.broker_request("/0/private/AddOrder", {
        "nonce": str(int(1000 * time.time())),
        "ordertype": "market",
        "type": "buy",
        "volume": buy_amount,
        "pair": "XBTUSD",
    }, constants.api_key, constants.api_sec)
    
    if not resp.json()['error']:
        print("Successfully bought BTC!")
    else:
        print(f"Error: { resp.json()['error'] }")

# Função que realiza a venda das cryptos      
def selling_currency(sell_amount):
    print(f"Selling {sell_amount} of BTC at {current_price}!")
    
    resp = broker_auth.broker_request("/0/private/AddOrder", {
        "nonce": str(int(1000 * time.time())),
        "ordertype": "market",
        "type": "sell",
        "volume": sell_amount,
        "pair": "XBTUSD",
    }, constants.api_key, constants.api_sec)
    
    if not resp.json()['error']:
        print("Successfully sold BTC!")
    else:
        print(f"Error: { resp.json()['error'] }")

# Realiza a troca de moedas        
def make_exchange():
    return

# Cancela todas as operações
def stop_operations():
    return
