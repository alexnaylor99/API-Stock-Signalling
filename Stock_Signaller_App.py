# Import packages
# import os
import requests
import time
# from dotenv import load_dotenv

# Load environment variables from .env file 
# load_dotenv()

# API_KEY = os.environ['API_KEY']
# PRICE_DROP_KEY = os.environ['PRICE_DROP_KEY']
# average_drop_key = os.environ['AVERAGE_DROP_KEY']

# Replace with your IFTTT Webhooks keys and event names
price_drop_key = 'hk1XqN9c6Lf3fny61cgEOLQb3L_J71xc5h2WpNu9MmP'
price_drop_event = 'sp_25p_alert' 
# average_drop_key="hk1XqN9c6Lf3fny61cgEOMkLhEGT8CNupRK-3l5KgWy"
average_drop_event = 'sp_7da_alert'

# Define a list of stock symbols you want to monitor
stock_symbols = ["TSLA", "AAPL", "GOOGL", "MSFT", "NKE"]

# Dictionaries to store data
last_prices = {}
seven_day_averages = {}

# Define the max number of API calls before stopping
max_api_calls = 1  # Change this to your desired limit

# Counter to keep track of API calls
api_call_count = 0

def send_webhook_alert(event_key, event_name, message):
    # Send a webhook alert
    url = f'https://maker.ifttt.com/trigger/{event_name}/with/key/hk1XqN9c6Lf3fny61cgEOMkLhEGT8CNupRK-3l5KgWy'
    playload = {'value1': message}
    response = requests.post(url, data=playload)
    if response.status_code == 200:
        print(f"Alert sent successfully to {event_name}.")
    else:
        print(f"Failed to send alert to {event_name}. Status code: {response.status_code}")

def fetch_stock_data(symbol):
    try:
        # Fetch intraday data - fix .env ->
        intraday_url = 'https://financialmodelingprep.com/api/v3/quote-short/AAPL,GOOGL,TSLA,MSFT,NKE?apikey=151bf0b888c3544b249779155b5233a9'
        intraday_data = requests.get(intraday_url).json()
        for element in intraday_data:
            print('Here is the real time stock price for: ' f"{element['symbol']}: {element['price']}")
  

        # Fetch daily data - fix .env ->
        daily_url = 'https://financialmodelingprep.com/api/v3/historical-price-full/AAPL,GOOGL,TSLA,MSFT,NKE?serietype=line&apikey=151bf0b888c3544b249779155b5233a9'
        daily_data = requests.get(daily_url).json()
        daily_prices = daily_data['historicalStockList']
        
        # Calculate the 7-day average
        # daily_prices_list = [float(daily_prices[date]['4. close']) for date in list(daily_prices.keys())[:7]]
        daily_prices_list = [float(entry["close"]) for entry in daily_data["historicalStockList"][0]["historical"]]
        seven_day_average = sum(daily_prices_list) / len(daily_prices_list)
        for element in seven_day_average:
            print('Here is the seven-day average stock price for: ' f"{element['symbol']}: {element['seven_day_average']}")

        return latest_price, seven_day_average

    except KeyError:
        # Handle missing data in the API response
        print(f"Data not available for {symbol}.")
        return None, None

    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred while fetching data for {symbol}: {str(e)}")
        return None, None



while True:
    try:
        for symbol in stock_symbols:
            latest_price, seven_day_average = fetch_stock_data(symbol)

            if latest_price is not None:
                # Check for price drop and 7-day average as before
                if symbol in last_prices:
                    price_drop = last_prices[symbol] - latest_price
                    if price_drop >= 0.25:
                        message = f"{symbol} Alert: Price Drop of £0.25 or More\nCurrent Price: £{latest_price:.2f}"
                        send_webhook_alert(price_drop_key, price_drop_event, message)

                if latest_price < seven_day_averages.get(symbol, latest_price):
                    message = f"{symbol} Alert: Price Fell Below 7-Day Average\nCurrent Price: £{latest_price:.2f}, 7-Day Avg: £{seven_day_average:.2f}"
                    send_webhook_alert(average_drop_key, average_drop_event, message)

                # Update last_prices and seven_day_averages as before
                last_prices[symbol] = latest_price
                seven_day_averages[symbol] = seven_day_average

                # Print stock data
                print(f"{symbol}: £{latest_price:.2f} (7-Day Avg: £{seven_day_average:.2f})")

        # API call count (useful for accounts with call limit)
        api_call_count += 1

        # Sleep for a few seconds before fetching data again
        time.sleep(6000)  # Adjust the interval as needed

    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
        break
    except Exception as e:
        print(f"An error occurred: {str(e)}")