import requests
import time
from json.decoder import JSONDecodeError
import os
from dotenv import load_dotenv
from collections import deque

load_dotenv()


class StockInfo:
    def __init__(self, symbol):
        self.symbol = symbol
        self.current_price = None
        self.previous_price = None
        self.seven_day_prices = deque(maxlen=7)

    def update_price(self, new_price):
        self.previous_price = self.current_price
        self.current_price = new_price

    def update_seven_day_prices(self, daily_average):
        self.seven_day_prices.append(daily_average)

    def calculate_seven_day_average(self):
        if len(self.seven_day_prices) == 0:
            return None
        return sum(self.seven_day_prices) / len(self.seven_day_prices)

    def check_price_fall(self):
        if self.current_price and self.previous_price:
            if self.current_price < self.previous_price - 0.25:
                print(
                    f"ALERT: {self.symbol} has fallen by at least £0.25 GBP. Current price is ${self.current_price}. Time to buy!"
                )

    def check_below_seven_day_avg(self):
        seven_day_avg = self.calculate_seven_day_average()
        if (
            seven_day_avg is not None
            and self.current_price is not None
            and self.current_price < seven_day_avg
        ):
            print(
                f"ALERT: {self.symbol}'s current price of ${self.current_price} is below the 7-day average of ${seven_day_avg}. Consider buying!"
            )


def get_stock_price(symbol, api_token):
    url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={api_token}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            return float(data[0]["price"])
        except (JSONDecodeError, KeyError):
            print(f"Failed to get price data for {symbol}.")
            return None


def get_daily_average_price(symbol, api_token):
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?timeseries=7&apikey={api_token}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()["historical"]
            prices = [day["close"] for day in data]
            return sum(prices) / len(prices)
        except (JSONDecodeError, KeyError):
            print(f"Failed to get historical data for {symbol}.")
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
            daily_avg = get_daily_average_price(stock_info.symbol, api_token)

            if new_price is not None:
                stock_info.update_price(new_price)
                if daily_avg is not None:
                    stock_info.update_seven_day_prices(daily_avg)

                stock_info.check_price_fall()
                stock_info.check_below_seven_day_avg()

        time.sleep(60 * 5)  # Sleep for 5 minutes
