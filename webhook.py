import requests

import os
from dotenv import load_dotenv


load_dotenv()


def send_ifttt_webhook(event, symbol, current_price, previous_price):
    webhook_key = os.getenv("WEBHOOK_KEY")
    url = f"https://maker.ifttt.com/trigger/{event}/with/key/{webhook_key}"
    payload = {
        "value1": symbol,
        "value2": str("{:.2f}".format(round(current_price, 2))),
        "value3": str("{:.2f}".format(round(previous_price, 2))),
    }
    response = requests.post(url, json=payload)
