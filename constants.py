from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

api_key = os.getenv("API_KEY")
api_sec = os.getenv("API_SEC")
api_url_broker = os.getenv("API_CORR")
api_url_awesome = os.getenv("API_REAL")

# Caminho dos dados
json_data_path = os.getenv("JSON_DATA")
csv_history_day = os.getenv("CSV_HIST_DAY")
csv_history_week = os.getenv("CSV_HIST_WEEK")
csv_history_month = os.getenv("CSV_HIST_MONTH")
csv_history_year = os.getenv("CSV_HIST_YEAR")

# Datas de analize
one_days_ago = (datetime.now() - timedelta(days=1)).date().isoformat()
seven_days_ago = (datetime.now() - timedelta(days=7)).date().isoformat()
thirty_days_ago = (datetime.now() - timedelta(days=30)).date().isoformat()
one_year_ago = (datetime.now() - timedelta(days=365)).date().isoformat()
atual_date = datetime.now().date().isoformat()
