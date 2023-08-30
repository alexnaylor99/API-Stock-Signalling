import requests
import datetime
import schedule
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Adjust the logging level as and when required

# IFTTT Webhooks details
ifttt_event_name = "update_stock_prices"
ifttt_api_key = "dFtK3DkhVCFf5_NqCxS1HH"
base_url = "https://financialmodelingprep.com/api/v3"
api_key = "733e442a1ef9374542a43ce72e65adf9"

# List of stocks to monitor
stocks = ["TSLA", "AAPL", "MSFT", "GOOGL", "NKE"]

MIN_PRICE_DIFFERENCE = 0.25


def get_stock_price(symbols):
    url = f"{base_url}/quote-short/{', '.join(symbols)}?apikey={api_key}&datatype=csv"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.text.splitlines()
        headers = data[0].split(',')
        values = data[1].split(',')

        # Find the index of the "price" column
        price_index = headers.index('price')

        if len(values) > price_index:
            print("Successfully retrieved stock data:")
            print(data)
            return float(values[price_index])
        else:
            print("Data format is unexpected:")
            print(data)
            return None
    else:
        print(f"Failed to retrieve stock data. Status code: {response.status_code}")
        return None


def calculate_7_day_average(symbol):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)
    url = f"{base_url}/historical-price-full/{symbol}?from={start_date}&to={end_date}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if "historical" in data:
        prices = [item["close"] for item in data["historical"]]
        return sum(prices) / len(prices)
    else:
        return None


previous_prices = {}


# Function to calculate price change


def calculate_price_change(symbol, current_price):
    if symbol in previous_prices:
        previous_price = previous_prices[symbol]
        return current_price - previous_price
    else:
        return 0.0  # Default value for the first time


def fetch_and_send_data():
    stock_data = []

    for stock_symbol in stocks:
        current_price_gbp = get_stock_price([stock_symbol])  # Fetch price in GBP
        current_price_usd = convert_usd_to_gbp(current_price_gbp)  # Convert to GBP for comparison
        average_price_gbp = calculate_7_day_average(stock_symbol)  # Fetch average price in GBP

        if current_price_gbp is not None:
            price_change_gbp = calculate_price_change(stock_symbol, current_price_gbp)

            if price_change_gbp <= -MIN_PRICE_DIFFERENCE:
                stock_data.append({
                    'name': stock_symbol,
                    'current_price': current_price_gbp,
                    'price_change': price_change_gbp,
                    'average_price': average_price_gbp,
                })

            previous_prices[stock_symbol] = current_price_gbp

    if stock_data:
        send_to_ifttt_webhook(stock_data)
    else:
        logging.info("The stock prices remain unchanged")

def convert_usd_to_gbp(usd_amount):
    conversion_rate = 1.35
    return usd_amount / conversion_rate


# Function to send data to IFTTT webhook
def send_to_ifttt_webhook(data_list):
    url = f"https://maker.ifttt.com/trigger/update_prices/json/with/key/{ifttt_api_key}"
    response = requests.post(url, json=data_list)

    if response.status_code == 200:
        logging.info("Webhook triggered successfully.")
    else:
        logging.error("Failed to trigger webhook. Status code: %d", response.status_code)


# Define a function to run the scheduled job
def run_scheduled_job():
    print("Fetching and sending data...")
    fetch_and_send_data()
    print("Job completed.")


schedule.every().day.at("09:00").do(fetch_and_send_data)
# Schedule the job to run every 5 seconds
schedule.every(5).seconds.do(run_scheduled_job)

# Run the scheduling loop
while True:
    schedule.run_pending()
    time.sleep(1)