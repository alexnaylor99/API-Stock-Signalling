import yfinance as yf
import requests
import time
import pandas as pd

IFTTT_EVENT_NAME = 'stock_has_dropped'
IFTTT_KEY = 'b8wRX9xgqi7o9u43AAlmwA'

# Calculate the 7-day average of stock prices
def calculate_7_day_average(ticker_symbol):
    today = pd.Timestamp.now()
    seven_days_ago = today - pd.DateOffset(days=7)

    data = yf.download(ticker_symbol, start=seven_days_ago, end=today)
    return data['Close'].mean()

# Get the current stock price
def get_stock_price(ticker_symbol):
    stock_data = yf.Ticker(ticker_symbol)
    return stock_data.history(period='1d')['Close'].iloc[0]

# Main function
def main():
    ticker_symbol = {'AAPL': 0,
                     'TSLA': 0,
                     'MSFT': 0,
                     'GOOGL': 0,
                     'NKE': 0} 
    previous_price = None
    current_price = None

    # Getting new current price, updating previous price and seven day average
    while True:
        for stock in ticker_symbol:
            previous_price = ticker_symbol[stock]
            current_price = get_stock_price(stock)
            seven_day_average = calculate_7_day_average(stock)
            ticker_symbol[stock] = current_price

        price_difference = previous_price - current_price

        if price_difference >= 0.30 or current_price < seven_day_average:
            # Trigger IFTTT applet using Webhooks service
            payload = {'value1': current_price, 'value2': seven_day_average}
            requests.post(f'https://maker.ifttt.com/trigger/{IFTTT_EVENT_NAME}/json/with/key/{IFTTT_KEY}', json=payload)
        
    
        previous_price = current_price
        # Check every 5 minutes
        time.sleep(300)  

if __name__ == "__main__":
    main()
