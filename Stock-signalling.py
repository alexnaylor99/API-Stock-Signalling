import requests


# List ofstock symbols that will be monitored
stock_symbols = {"TSLA":0, "AAPL":0, "MSFT":0, "GOOGL":0, "NKE":0}

# API key and the base URL
alpha_vantage_api_key = "NZXLRSMAPCX4T3YW"
base_url = "https://www.alphavantage.co/query"

# IFTTT Webhook URL
ifttt_webhook_url = "https://maker.ifttt.com/trigger/stock-price-decrease/json/with/key/bWs2poP5Q2RliJ9-PmAYcbb"

# Dictionary will store the previous stock prices
previous_prices = {}
previous_price = 0 

def get_stock_price(symbol):
   # Get the daily closing stock price for a given symbol using the Alpha Vantage API.
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": alpha_vantage_api_key
        }
    for symbol in stock_symbols:
        stock_price = get_stock_price(symbol)
        previous_price = previous_prices.get(symbol, None)
        response = requests.get(base_url, params=params)
        data = response.json()
        return float(data["Time Series (Daily)"][list(data["Time Series (Daily)"].keys())[0]]["4. close"])


def send_notification(stock_symbol, stock_price, previous_price):
    if  previous_price - stock_price >= 0.25:
        message = f"{stock_symbol} price decreased by £0.25: {stock_price}"
        data = {
            "value1": message
        }
        response = requests.post(ifttt_webhook_url, json=data)
        if response.status_code == 200:
            print(f"Notification sent for {stock_symbol}")
        else:
            print(f"Notification failed for {stock_symbol}")

    # Update the previous price in the dictionary
        previous_prices[symbol] = stock_price


if __name__ == "__main__":
    for symbol in stock_symbols:
        stock_price = get_stock_price(symbol)
        previous_price = previous_prices.get(symbol, None)

        send_notification(symbol, stock_price, previous_price)


