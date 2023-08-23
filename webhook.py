import requests

import os
from dotenv import load_dotenv
import json

load_dotenv()


def send_ifttt_webhook(event, symbol, current_price, previous_price):
    webhook_key = os.getenv("WEBHOOK_KEY")
    url = f"https://maker.ifttt.com/trigger/{event}/json/with/key/{webhook_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "symbol": symbol,
        "previous_price": str(previous_price),
        "current_price": str(current_price),
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
