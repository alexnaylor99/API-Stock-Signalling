"""
This script monitors specified stocks, compares their prices with historical averages,
and sends email notifications when certain conditions are met.
"""

#Import the necessary libraries and modules
import yfinance as yf
import smtplib
import schedule
import time
import os
from forex_python.converter import CurrencyRates
from dotenv import load_dotenv
from statistics import mean

# Load environment variable from .env file
load_dotenv()

# Initialize currency converter
currency_converter = CurrencyRates()

# Define the stocks to monitor and the email details
stocks_to_monitor = ["AAPL", "MSFT", "GOOGL", "TSLA", "NKE"]
previous_prices = {ticker: 0 for ticker in stocks_to_monitor}

#Set-up your own environment .env (README)
email_user = os.environ.get('EMAIL_USER')
receiver_email = os.environ.get('RECEIVER_EMAIL')

#Error Handling (in case user forgets setring-up .env)
try:
    email_pass = os.environ['EMAIL_PASS']
except KeyError:
    print("EMAIL_PASS environment variable not found. Check README")
    exit(1)

# Return a yfinance Ticker object for the given symbol
def process_tickers():
    for ticker in stocks_to_monitor:
        stock = yf.Ticker(ticker)  # Directly instantiate yf.Ticker within the loop
        check_seven_day_avg(stock, ticker)
        check_one_minute_price_change(stock, ticker)

# Handling the price retrieval and conversion to GBP
def get_current_price(stock):
    current_price_usd = stock.info['currentPrice']
    current_price_gbp = currency_converter.convert('USD', 'GBP', current_price_usd)
    return current_price_gbp

# Fetch the last 7 days of price data, calculate the average and prepare message
def check_seven_day_avg(stock, ticker):
    hist = stock.history(period="7d")
    avg = mean(hist["Close"])
    avg_gbp = currency_converter.convert('USD', 'GBP', avg)
    
    current_price_gbp = get_current_price(stock)
    if current_price_gbp < avg_gbp:
        subject = f'Price Alert for {ticker}'
        body = f'The current price of {ticker} is below the 7-day average, at {current_price_gbp} GBP.'
        send_notification(subject, body)

def check_one_minute_price_change(stock, ticker):
    current_price_gbp = get_current_price(stock)
    previous_price_gbp = currency_converter.convert('USD', 'GBP', previous_prices[ticker])
    diff = previous_price_gbp - current_price_gbp
    if diff >= 0.01:
        subject = f'Price Drop Alert for {ticker}'
        body = f'The price of {ticker} has dropped to {current_price_gbp} GBP.'
        send_notification(subject, body)
        
        # Store the price in USD for the next check
        previous_prices[ticker] = stock.info['currentPrice']  # Fetching the current price in USD again.

# Send an email notification
def send_notification(subject, body):
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_user, email_pass)
            msg = f'Subject: {subject}\n\n{body}'
            server.sendmail(email_user, receiver_email, msg)
    except Exception as e:
        print(f"Error sending email: {e}")            

# Schedule the process_tickers function to run every minute
schedule.every(1).minutes.do(process_tickers)

while True:
    schedule.run_pending()
    time.sleep(1)