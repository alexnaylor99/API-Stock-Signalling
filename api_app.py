import requests
import time
from json.decoder import JSONDecodeError
import os
from dotenv import load_dotenv

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


def get_stock_price(symbol, api_token):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_token}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            latest_close_price = list(data["Time Series (5min)"].values())[0][
                "4. close"
            ]
            return float(latest_close_price)
        except JSONDecodeError:
            print(f"Could not decode JSON response for symbol {symbol}.")
            return None
        except KeyError:
            print(f"Could not find necessary data for symbol {symbol}.")
            return None
    else:
        print(
            f"Failed to retrieve stock data for {symbol}. HTTP Status Code: {response.status_code}"
        )
        return None


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

        time.sleep(60)  # Pause for 60 seconds before the next round of checks
