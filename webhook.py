import requests

import os
from dotenv import load_dotenv

load_dotenv()


def send_ifttt_webhook(event, symbol, current_price, previous_price):
    webhook_key = os.getenv("WEBHOOK_KEY")
    url = f"https://maker.ifttt.com/trigger/{event}/with/key/{webhook_key}"
    payload = {"value1": symbol, "value2": current_price, "value3": previous_price}
    print(f"Sending payload: {payload}")
    response = requests.post(url, json=payload)
    print(f"Received response: {response.text}")
