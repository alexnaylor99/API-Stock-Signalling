import requests
import json

def get_dataset(ticker):
    """
    A function that fetches an api based on ticker value (sybmbol of company) whic
    then returns a dictionary data structure 
    """
    print("Running dataset")
    response_for_realtime = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=1min&outputsize=compact&apikey=O3KE4N17RB5IPQOD")
    if response_for_realtime.status_code == 200:
        data = response_for_realtime.json()
        print(data)
        return data
    
    else:
        print("Error getting the request needed: ", response_for_realtime.status_code)

def get_main_data(dict):
    """
    A simple function that returns data belonging to the key 'Time Series (1min)
    """
    print("Getting main data")
    return dict['Time Series (1min)']

def get_datasets(ticker_list):
    """
    A function that takes in a list of tickers and calls the 
    function 'get_dataset()' and stores each dataset on to a list 
    then returns it.
    """
    print("Running datasets")
    datasets = []
    for ticker in ticker_list:
        temp_data = (get_dataset(ticker))
        datasets.append(get_main_data(temp_data))
    return datasets

def store_stock_price(stock_pair,new_price):
    """
    A functions that updates the prices.
    This function would be called when there has been an update on the prices.
    """
    stock_pair.pop(0)
    stock_pair.append(new_price)
    return stock_pair

def has_price_decreased(pair_of_stock_prices):
    """
    This function checks if the new stock price is below £0.25.
    The function will return True.
    This is called from the main function.
    """
    if float(pair_of_stock_prices[1]) < (float(pair_of_stock_prices[0]) - 0.25):
        return True


def generate_stock_queue(dict):
    """
    This function generates a pair of stock prices.
    It acts as a queue where when you push one price, then 
    push the most recent price on the list.
    It then converts to GBP which is what the stakeholder wants.
    """
    new_stock_pair = []
    latest_data_dict = list(dict.items())
    newest_price = latest_data_dict[0][1]['1. open']
    second_newest_price = latest_data_dict[1][1]['1. open']
    new_stock_pair.append(convert_usd_to_gbp(newest_price))
    new_stock_pair.append(convert_usd_to_gbp(second_newest_price))
    return new_stock_pair

def get_all_stock_pairs(datasets):
    """
    This function iterates each dataset to generate a stock pair
    for each company.
    It returns a two-dimensional array.
    """
    two_d_array_stock = []
    for dataset in datasets:
        two_d_array_stock.append(generate_stock_queue(dataset))
    return two_d_array_stock


def return_open_val(given_dict):
    # returns the open price for a given dataset
    return float(given_dict['1. open'])



def convert_usd_to_gbp(price_to_convert):
    # a simple function to convert USD to GBP
    return price_to_convert/1.23

def main():
    """
    The main calls all the functions above and communicates with the IFTTT so it can email
    any updates about the stocks when triggered.
    """
    api_key = "nmSjoGFt5z5ExJ4bLUMBcr0JozQykoHC2TB5dUNdUT4"
    event_name = "stock_update"
    url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{api_key}"

    real_time_stock_data = "real_time_data.json"
    
    TICKER_LIST = ["AAPL","TSLA","MSFT","GOOGL","NKE"]
    stock_datasets = []
    stock_pairs = []
    stock_datasets = get_datasets(TICKER_LIST)

    for dict in stock_datasets:
        stock_pairs.append(generate_stock_queue(dict))
    full_data_dict = {k: v for k, v in zip(TICKER_LIST, stock_pairs)}
    
    with open(real_time_stock_data, 'w') as f:
        json.dump(full_data_dict, f, indent=4)

    for key,value in full_data_dict.items():
        print(key, ':', value)
        if has_price_decreased(value):
            message = f"The stock price for {key} has dropped by at least £0.25GBP. Buy more stocks now!!!"
            data = {
                'Value1':message
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("Email sent!")
            else:
                print("Failed to send email.")
            print("Yes there has been a drop of prices")
        else: 
            data = {
                'Value1':'No updates on the stocks',
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("Email sent!")
            else:
                print("Failed to send email.")
            print("No decrease")
    
    
main()

    



