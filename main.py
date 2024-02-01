import time
import requests
import urllib.parse
import hashlib
import hmac
import base64

api_url = "https://api.kraken.com"
buy_limit = 0
sell_limit = 0
buy_amount = 0.01
sell_amount = 0.01

# Pega as chaves da conta do arquivo txt
with open("keys.txt", "r") as f:
    lines = f.read().splitlines()
    api_key = lines[0]
    api_sec = lines[1]
    
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
    resp = requests.post((api_url + url_path), headers=headers, data=data)
    return resp


while True:
    # Pega o preco atual da API publica
    current_price = requests.get("https://api.kraken.com/0/public/Ticker?pair=BTCUSD").json()['result']['XXBTZUSD']['c'][0]
    
    # 
    if float(current_price) < buy_limit:
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
            
    #        
    elif float(current_price) > sell_limit:
        print(f"Selling {buy_amount} of BTC at {current_price}!")
        
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
            
    #
    else:
        print(f"Current Price: {current_price}, not buying or selling")
    time.sleep(3)
