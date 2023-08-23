import requests
import time
from json.decoder import JSONDecodeError
import os
from dotenv import load_dotenv
from webhook import (
    send_ifttt_webhook,
)  # Assuming you have this function in a webhook.py file
import random  # Import the random module for generating test data

load_dotenv()


class StockInfo:
    def __init__(self, symbol):
        self.symbol = symbol
        self.current_price = None
        self.previous_price = None

    def update_price(self, new_price):
        self.previous_price = self.current_price
        self.current_price = new_price

    def check_price_fall(self):
        if self.current_price is not None and self.previous_price is not None:
            price_diff = self.current_price - self.previous_price
            if price_diff <= -0.25:
                print(
                    f"ALERT: {self.symbol} has fallen by at least £0.25 GBP. Current price is ${self.current_price}. Time to buy!"
                )
                send_ifttt_webhook(
                    "stock_price_fell",
                    self.symbol,
                    self.current_price,
                    self.previous_price,
                )


# Mock the get_stock_price function to use test data
def get_stock_price(symbol, api_token):
    return random.uniform(100, 200)  # Random float between 100 and 200


if __name__ == "__main__":
    api_token = os.getenv("API_KEY")

    monitored_stocks = [
        StockInfo("TSLA"),
        StockInfo("AAPL"),
        StockInfo("MSFT"),
        StockInfo("GOOGL"),
        StockInfo("NKE"),
    ]

    while True:
        for stock_info in monitored_stocks:
            new_price = get_stock_price(stock_info.symbol, api_token)
            if new_price is not None:
                print(f"Current price of {stock_info.symbol}: ${new_price}")
                stock_info.update_price(new_price)
                stock_info.check_price_fall()

        time.sleep(5)  # Pause for 60 seconds before the next round of checks
