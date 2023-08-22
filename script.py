import requests #module
import time

api_key = "2f20ea0a2f9b4a27bd2cd6b2464d6d60"

def get_stock_price(symbol):
    base_url = "https://api.twelvedata.com/price"

    params = {
            "symbol": symbol,
            "apikey": api_key

        }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "price" in data:
        return float(data["price"])
        
    else:
        return None

    

if __name__ == "__main__":
    stock_symbols = ["AAPL", "GOOGL", "MSFT" , "NKE", "TSLA"]
    

    for symbol in stock_symbols:
        stock_price = get_stock_price(symbol)

        if stock_price is not None:
            print(f"The latest price of {symbol} is ${stock_price:.2f}")

        else:
            print(f"Couldn't retrieve price for {symbol}")



    