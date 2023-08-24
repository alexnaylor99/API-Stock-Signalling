import requests

import os
from dotenv import load_dotenv


load_dotenv()


# Function to send a webhook to IFTTT
def send_ifttt_webhook(event, message):
    webhook_key = os.getenv("WEBHOOK_KEY")
    url = f"https://maker.ifttt.com/trigger/{event}/with/key/{webhook_key}"
    payload = {
        "value1": message,
        "value2": "",
        "value3": "",
    }
    response = requests.post(url, json=payload)


# Function to send a price drop alert
def send_price_drop(event, symbol, current_price, previous_price):
    message = f"ALERT: The stock {symbol} has fallen. Previous Price: ${previous_price:.2f}. Current Price: ${current_price:.2f}. Consider buying now!"
    send_ifttt_webhook(event, message)


# Function to send an alert when the price is below the 7-day average
def send_avg_price_drop(event, symbol, current_price, daily_avg):
    message = f"ALERT: {symbol}'s current price of ${current_price:.2f} is below the 7-day average of ${daily_avg:.2f}. Consider buying!"
    send_ifttt_webhook(event, message)
