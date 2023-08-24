import requests
import time
import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

WEBHOOKS_KEY = os.getenv('WEBHOOKS_KEY')



IFTTT_URL = f"https://maker.ifttt.com/trigger/notify/with/key/{WEBHOOKS_KEY}"



PRICE_DROP_THRESHOLD = 0.25

stock_symbols = ["AAPL", "GOOGL", "MSFT" , "NKE", "TSLA"]

previous_prices = {}



#function that returns latest stock prices
def get_stock_price(symbol):
    url = f"https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data['latestPrice']


#function that sends IFTTT notification
def send_notification(symbol, price):
    
    payload = {
        "value1" : symbol,
        "value2" : str(price)
    }

    requests.post(IFTTT_URL, json=payload)
  
    

if __name__ == "__main__":
    while True:
        try:
            for symbol in stock_symbols:
                current_stock_price = get_stock_price(symbol)
                print(f"The latest price of {symbol} is {current_stock_price:} GBP")

                if current_stock_price <= (get_stock_price(symbol) - PRICE_DROP_THRESHOLD):
                    send_notification(symbol, current_stock_price)
                    print(f"{symbol} price dropped by at least £0.25 GBP.")

              
            
            time.sleep(300)
        
        except Exception as e:
            print("ERROR!", e)
