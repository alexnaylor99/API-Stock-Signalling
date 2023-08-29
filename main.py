import requests
import time

# API key with IEX Cloud
api_key = "pk_c2257f70a6584faca4bb653bd4618478"

# Stocks to monitor
stocks = ["TSLA", "AAPL", "MSFT", "GOOGL", "NKE"]

# IFTTT Webhook URL for £0.25 price drop
IFTTT_webhook_url = "https://maker.ifttt.com/trigger/stock_price_falls/with/key/hKArh7xueLrGZEGnVP-IB4nYOdWZ3bR-hiMDYmTt283"

# IFTTT Webhook URL for 7-day average fall
IFTTT_7day_average_webhook_url = "https://maker.ifttt.com/trigger/7day_average/with/key/hKArh7xueLrGZEGnVP-IB4nYOdWZ3bR-hiMDYmTt283"

# Create a dictionary to store previous prices for each week
previous_prices = {}

# Function to fetch stock prices
def get_stock_price(symbol):
    url = f"https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={api_key}"
    response = requests.get(url)
    data = response.json()
    return float(data["latestPrice"])

# Function to fetch 7-day average price
def get_7day_average(symbol):
    url = f"https://cloud.iexapis.com/stable/stock/{symbol}/chart/1w?token={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if data:
        prices = [float(entry["close"]) for entry in data]
        average = sum(prices) / len(prices)
        return average
    else:
        print(f"Error fetching 7-day average for {symbol}: {data}")
        return None

# Function to send IFTTT notification for £0.25 price drop
def send_notification(stock_symbol, price):
    payload = {
        "value1": stock_symbol,
        "value2": str(price)
    }
    requests.post(IFTTT_webhook_url, json=payload)

# Function to send IFTTT notification for 7-day average price drop
def send_7day_average_notification(stock_symbol):
    payload = {
        "value1": stock_symbol,
        "value3": "Today's price is lower than 7-day average."
    }
    requests.post(IFTTT_7day_average_webhook_url, json=payload)

# Main monitoring loop
while True:
    print("Monitoring stock prices...")

    for stock_symbol in stocks:
        current_price = get_stock_price(stock_symbol)
        average_7day = get_7day_average(stock_symbol)
    
        if stock_symbol in previous_prices:
            price_change = previous_prices[stock_symbol] - current_price
            
            if price_change >= 0.25: 
                send_notification(stock_symbol, f"Fell by £{price_change:.2f} or more.")
                print(f"{stock_symbol} price fell by £0.25 or more. Sending notification.")
            
            if average_7day is not None and current_price < average_7day:
                send_7day_average_notification(stock_symbol)
                print(f"{stock_symbol} price is lower than 7-day average. Sending notification.")
        
        previous_prices[stock_symbol] = current_price
    
    # Check every 1 minute 
    time.sleep(60)



