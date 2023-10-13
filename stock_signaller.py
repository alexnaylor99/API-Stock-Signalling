import requests

# Stock API access parameters
BASE_URL = "https://api.twelvedata.com"
API_KEY = "a234819a7d95480cac20af90c630e0b9"

# IFTTT named events that trigger email sending
EVENT_WEEKLY_AVERAGE = "price_less_than_weekly_average"
EVENT_PRICE_DROP = "stock_price_25p_drop"

# IFTTT general webhook URL --> different event names for either stock
# price event
IFTTT_WEBHOOK_URL = (
    "https://maker.ifttt.com/trigger/{event_name}/json/with/key/i9fIToN8DAw1mChzvPMK1"
)


def get_exchange_rate():
    """
    Obtains and returns the latest USD to GBP exchange rate from
    TwelveData API
    """
    endpoint = (
        f"{BASE_URL}/time_series?"
        f"symbol=USD/GBP&interval=1min&apikey={API_KEY}"
    )
    response = requests.get(endpoint)
    data = response.json()
    latest_data = data['values'][0]
    return float(latest_data['close'])


def get_stock_price(company, exchange_rate):
    """
    Obtains and returns the current stock price for desired stock
    """
    endpoint = (
        f"{BASE_URL}/time_series?"
        f"symbol={company}&interval=1min&apikey={API_KEY}"
    )
    response = requests.get(endpoint)
    data = response.json()
    latest_data = data['values'][0]
    usd_price = float(latest_data['close'])
    return usd_price * exchange_rate


def get_previous_stock_price(company, exchange_rate):
    """
    Obtains and returns the stock price for desired stock from 1 minute
    ago
    """
    endpoint = (
        f"{BASE_URL}/time_series?"
        f"symbol={company}&interval=1min&apikey={API_KEY}"
    )

    response = requests.get(endpoint)
    data = response.json()
    previous_data = data['values'][1]
    usd_price = float(previous_data['close'])
    return usd_price * exchange_rate


def get_seven_day_average(company, exchange_rate):
    """
    Obtains and returns the stock price of the desired stock, at market
    closing time from past seven days and calculates weekly average
    """
    endpoint = (
        f"{BASE_URL}/time_series?"
        f"symbol={company}&interval=1day&apikey={API_KEY}"
    )
    response = requests.get(endpoint)
    data = response.json()
    last_seven_days = data['values'][:7]
    total = 0
    for day in last_seven_days:
        total += float(day['close']) * exchange_rate
    return total / 7


def send_notification(event_name, stock_symbol):
    """
    Sends notification to relevant IFTTT applet
    """
    url = IFTTT_WEBHOOK_URL.format(event_name=event_name)
    data = {"Stock Name": stock_symbol}
    requests.post(url, json=data)


def check_and_notify(company):
    """
    Implements all requests to TwelveData API and defines stock
    price conditionals to be checked
    """
    exchange_rate = get_exchange_rate()
    current_price = get_stock_price(company, exchange_rate)
    previous_price = get_previous_stock_price(company, exchange_rate)
    seven_day_average = get_seven_day_average(company, exchange_rate)

    if current_price < seven_day_average:
        send_notification(EVENT_WEEKLY_AVERAGE, company)
        print(f"Notification sent for {EVENT_WEEKLY_AVERAGE} - {company}")

    if (previous_price - current_price) > 0.25:
        send_notification(EVENT_PRICE_DROP, company)
        print(f"Notification sent for {EVENT_PRICE_DROP} - {company}")


if __name__ == "__main__":
    stocks_to_check = ['AAPL', 'TSLA']
    for stock in stocks_to_check:
        check_and_notify(stock)


