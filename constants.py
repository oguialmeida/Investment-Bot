from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

api_key = os.getenv("API_KEY")
api_sec = os.getenv("API_SEC")
api_url_broker = os.getenv("API_CORR")
api_url_awesome = os.getenv("API_REAL")