import os
import json
import requests
from dotenv import load_dotenv
from td.client import TDClient

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
REDIRECT_URI = os.getenv('REDIRECT_URI')
CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH')

TDSession = TDClient(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    credentials_path=CREDENTIALS_PATH
)

TDSession.login()

print(TDSession.get_quotes(instruments=['AAPL']))