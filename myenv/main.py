import sys
sys.path.append('/path/to/yfinance') # I had trouble importing yfinance at first.
import yfinance as yf # Library where I can fetch stocks data.
import requests # To interact with web services like IFTTT.
import time # Provide functions related to time and delays.

# The event name I set up in my IFTTT applet.
ifttt_event_name = 'stock_price_drop'

# My IFTTT webhook key.
ifttt_webhook_key = 'hThx0WApHyDPrZzRnUlxAv0QMkIUfB55haBlJWd5kIC'

# The ticker symbols of the stocks I am monitoring, I can add or remove as needed.
stocks = ['TSLA', 'AAPL', 'MSFT', 'GOOGL', 'NKE']

# This is a dictionary that stores the previous prices of the stocks.
previous_prices = {}

'''This function fetches the current stock price. I used the parameter stock, so I can get individual stock prices. 
I have to index with:.iloc, if not an alert appears, warning that method of indexing may change in a future Pandas version. It suggests using the iloc method to ensure it is compatible with future versions. '''
def get_stock_price(stock):
    stock_data = yf.Ticker(stock)
    price = stock_data.history(period='1d')['Close'].iloc[0] # I had to add .iloc here (explained above).
    return price

# Similar to above, this time I want price for the last 7 days, I used the mean function to get the average.
def calculate_7_day_average(stock):
    stock_data = yf.Ticker(stock)
    historical_data = stock_data.history(period='7d')
    return historical_data['Close'].mean()

# Check if prices fall by £0.25 or more and notify me using the IFTTT applet, round prices to 2 decimal places.
def send_price_drop_notification(stock, current_price):
    notification = {'value1': f'{stock} stock price fell by at least £0.25. Current price: £{current_price:.2f}'}
    url = f'https://maker.ifttt.com/trigger/{ifttt_event_name}/with/key/{ifttt_webhook_key}'
    response = requests.post(url, json=notification)
    print(f'Notification sent: {notification}')
    print('£' * 50)

# Similar to above but will notify me when prices are below the seven day average.
def send_average_drop_notification(stock, current_price, seven_day_average):
    notification = {'value2': f'{stock} below 7 day average. 7 day average: {seven_day_average:.2f} Current price: £{current_price:.2f}'}
    url = f'https://maker.ifttt.com/trigger/{ifttt_event_name}/with/key/{ifttt_webhook_key}'
    response = requests.post(url, json=notification)
    print(f'Notification sent: {notification}')
    print('*' * 50)

'''By creating a while loop I can run my code every 60 seconds as long as the conditions inside this loop are true. '''
while True:
    for stock in stocks:
        # Stored my fetch price function in a variable.
        current_price = get_stock_price(stock)
        print(f'{stock}: {current_price:.2f}')

        # Stored my 7 day average function in a variable.
        seven_day_average = calculate_7_day_average(stock)
        print(f'7-day Average for {stock}: {seven_day_average:.2f}')

        # Check if both conditions are met, then notify me.
        if stock in previous_prices and current_price <= previous_prices[stock] - 0.25:
            send_price_drop_notification(stock, current_price)

        # Update the previous price in the dictionary to the current price.
        previous_prices[stock] = current_price

        # Check if the current price is less than 7 day average and notify me.
        if current_price < seven_day_average:
            send_average_drop_notification(stock, current_price, seven_day_average)

    print('-' * 50)
    time.sleep(60)
