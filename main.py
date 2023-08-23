import requests
import time

#Twelve Data API Key
API_KEY = "2f20ea0a2f9b4a27bd2cd6b2464d6d60"


WEBHOOKS_KEY = "b-gntgVdhCa1F8DgkWXRvT"


PRICE_FALL_THRESHOLD = 0.25



#function that returns latest stock prices
def get_stock_price(symbol):
    
    params = {
        "symbol": symbol,
        "apikey": API_KEY
    }

    response = requests.get("https://api.twelvedata.com/price", params=params)
    data = response.json()

    if "price" in data:
        return float(data["price"])

    else:
        return None

#function that sends IFTTT notification

def send_notification(stock_symbol, price):
    ifttt_url = "https://maker.ifttt.com/trigger/notify/json/with/key/b-gntgVdhCa1F8DgkWXRvT"

    data = {
        "value1" : stock_symbol,
        "value2" : price
    }

    response = requests.post(ifttt_url, json=data)

    if response.status_code == 200:
        print(f"Notification has been sent for {stock_symbol}.")
    
    else:
        print(f"Failed to send notification for {stock_symbol}.")


    

if __name__ == "__main__":
    stock_symbols = ["AAPL", "GOOGL", "MSFT" , "NKE", "TSLA"]

    for symbol in stock_symbols:
        current_stock_price = get_stock_price(symbol)

        if current_stock_price is not None:
            print(f"The latest price of {symbol} is ${current_stock_price:.2f}")
        
        else:
            print(f"Couldn't retrieve latest price for {symbol}")