import urllib.parse
import hashlib
import hmac
import base64
import requests
import constants

# Cria uma assinatura com base na chave
def get_broker_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message  = urlpath.encode() + hashlib.sha256(encoded).digest()
    
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    
    return sigdigest.decode()

# Autentica e deixa pronta a url para ser usada com os endpoints
def broker_request(url_path, data, api_key, api_sec):
    headers = {"API-Key": api_key, "API-Sign": get_broker_signature(url_path, data, api_sec)}
    resp = requests.post((constants.api_url_broker + url_path), headers=headers, data=data)
    return resp