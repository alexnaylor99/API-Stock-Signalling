# Import packages
import requests
import time

# Insert API key
api_key = 'YOUR_API_KEY'

# Define list of stock tickers you want to monitor
stock_symbols = ["TSLA", "AAPL", "MSFT", "GOOGL", "NKE"]

while True:
    try:
        for symbol in stock_symbols:
            # Construct the API URL
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={api_key}'

            # Make a GET request to the API and get the latest price directly
            latest_price = requests.get(url).json()['Time Series (1min)'][list(data['Time Series (1min)'].keys())[0]]['4. close']

            # Print the stock symbol and its latest price
            print(f"{symbol}: ${latest_price}")

        # Sleep for a few seconds before fetching data again
        time.sleep(10)  # You can adjust the interval as needed

    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
        break
    except Exception as e:
        print(f"An error occurred: {str(e)}")
