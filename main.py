import requests
import time
import datetime

# API base URL
BASE_URL = "https://financialmodelingprep.com/api/v3"

# API key (API from Financial Modeling Prep API Documentation)
API_KEY = "d5031e8e27160bf572aeeb965a8b0a2f"

# List of stocks to monitor
stocks = ["TSLA", "AAPL", "MSFT", "GOOGL", "NKE"]

# Threshold for price drop (£0.25 GBP)
PRICE_THRESHOLD = 0.1

# Function to get the current stock price
def get_stock_price(symbol):
    url = f"{BASE_URL}/quote-short/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data[0]["price"]

# Function to calculate 7-day average price
def calculate_7_day_average(symbol):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)
    url = f"{BASE_URL}/historical-price-full/{symbol}?from={start_date}&to={end_date}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    prices = [item["close"] for item in data["historical"]]
    return sum(prices) / len(prices)

# Function to send notification
def send_notification(stock_symbol, message):
    event_name = "stock_price_alert"
    payload = {
        "value1": stock_symbol,
        "value2": message
    }
    url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/YOUR_IFTTT_KEY"
    requests.post(url, json=payload)

# Main loop
if __name__ == "__main__":
    while True:
        for stock in stocks:
            current_price = get_stock_price(stock)
            average_price = calculate_7_day_average(stock)

            print("stock: ", stock)
            print("current_price: ", current_price)
            print("average_price: ", average_price)

            
            if current_price < average_price:
                message = f"Today's price ({current_price}) is less than 7-day average ({average_price})."
                send_notification(stock, message)
                
            if current_price <= (average_price - PRICE_THRESHOLD):
                message = f"Price dropped by at least £{PRICE_THRESHOLD} GBP. Current price: {current_price}"
                send_notification(stock, message)
                
        # Check every 5 minutes
        time.sleep(300)