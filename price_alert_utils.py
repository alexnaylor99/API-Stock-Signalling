import requests

def fetch_price_and_avg(symbol, base_iex_url, iex_api_key):
    endpoint = f"{base_iex_url}/stock/{symbol}/chart/5d?token={iex_api_key}"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()   
        data = response.json() 
        prices = [entry['close'] for entry in data]
        today_price = prices[-1]
        avg_7_day = sum(prices[:-1]) / len(prices[:-1])
        return today_price, avg_7_day
    except requests.RequestException as e:
        print(f"Error fetching data for {symbol}: {e}")
    except ValueError:
        print(f"Error decoding JSON for {symbol}")
    return None, None

def notify_ifttt(ifttt_webhook_key, event, value1="", value2="", value3=""):
    url = f"https://maker.ifttt.com/trigger/{event}/with/key/{ifttt_webhook_key}"
    data = {"value1": value1, "value2": value2, "value3": value3}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error notifying IFTTT: {e}")
        return response.status_code
