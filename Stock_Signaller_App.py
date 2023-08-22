# price drop url = https://maker.ifttt.com/use/hk1XqN9c6Lf3fny61cgEOLQb3L_J71xc5h2WpNu9MmP
# price drop key = hk1XqN9c6Lf3fny61cgEOLQb3L_J71xc5h2WpNu9MmP
# average drop url =https://maker.ifttt.com/use/hk1XqN9c6Lf3fny61cgEOMkLhEGT8CNupRK-3l5KgWy
# average drop key = hk1XqN9c6Lf3fny61cgEOMkLhEGT8CNupRK-3l5KgWy

# Import packages
import requests
import time

# API Key = YO4LSAY68E6AI3BB
api_key = 'YO4LSAY68E6AI3BB'

# Replace with your IFTTT Webhooks keys and event names
price_drop_key = 'YOUR_PRICE_DROP_WEBHOOKS_KEY'
price_drop_event = 'sp_25p_alert' 
average_drop_key = 'YOUR_AVERAGE_DROP_WEBHOOKS_KEY'
average_drop_event = 'sp_7da_alert'

# Define a list of stock symbols you want to monitor
stock_symbols = ["TSLA, AAPL,  GOOGL, MSFT, NKE"]

# Initialize dictionaries to store data
last_prices = {}
seven_day_averages = {}

def send_webhook_alert(event_key, event_name, message):
    # Send a webhook alert using the provided key and event name
    url = f'https://maker.ifttt.com/trigger/{event_name}/with/key/{event_key}'
    data = {'value1': message}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"Alert sent successfully to {event_name}.")
    else:
        print(f"Failed to send alert to {event_name}. Status code: {response.status_code}")

def fetch_stock_data(symbol):
    try:
        # Fetch intraday data
        intraday_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey=YOUR_API_KEY'
        intraday_data = requests.get(intraday_url).json()
        latest_prices = intraday_data['Time Series (1min)']
        latest_time = list(latest_prices.keys())[0]
        latest_price = float(latest_prices[latest_time]['4. close'])

        # Fetch daily data
        daily_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey=YOUR_API_KEY'
        daily_data = requests.get(daily_url).json()
        daily_prices = daily_data['Time Series (Daily)']

        # Calculate the 7-day average
        daily_prices_list = [float(daily_prices[date]['4. close']) for date in list(daily_prices.keys())[:7]]
        seven_day_average = sum(daily_prices_list) / len(daily_prices_list)

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

        # Sleep for a few seconds before fetching data again
        time.sleep(10)  # You can adjust the interval as needed

    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
        break
    except Exception as e:
        print(f"An error occurred: {str(e)}")