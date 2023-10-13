import requests
import json


def get_data_request(ticker):
    """
    This function fetches the api based on what company the ticker
    presents.
    Afterwards it gets the dictionary that has all the records of daily
    prices per day.
    Then, it makes sure to only take 5 records and returns the final dictionary.
    """
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&
            symbol={ticker}&outputsize=compact&apikey=demoY22ZX8DF9C8MCNWW"
    response_for_historical = requests.get(url)
    if response_for_historical.status_code == 200:
        data = response_for_historical.json()
        main_dict = data['Time Series (Daily)']
        finalized_dict = finalize_dict(main_dict)
        return finalized_dict
    else:
        print("Did not fetch data properly, ", 
              response_for_historical.status_code)
        


def store_weekly_avgs(ticker_list):
    """
    This function calculates the weekly average of a given 
    dataset then assigns it to its related symbol (company) 
    in form of a dictionary.
    """
    week_avgs = []
    for ticker in ticker_list:
        dataset = get_data_request(ticker)
        week_avgs.append(calc_weekly_average(dataset))
    return {k: v for k, v in zip(ticker_list, week_avgs)}


def finalize_dict(dict):
    """
    This function returns the first 5 items of the given 
    dictionary for its weekly calculation. 
    The reason 5 is because the stock market is only open 
    on weekdays.
    """
    first_five_items = {k: dict[k] for k in list(dict)[:5]}
    return first_five_items

def return_open_val(given_dict):
    # returns the open price of a given dictionary
    return float(given_dict['1. open'])

def calc_weekly_average(given_dict):
    # calculates the weekly average of a given dictionary
    total = 0
    for key, value in given_dict.items():
            total += return_open_val(value)
    return total/5

def latest_stock_lt_week_avg(stock_price, weekly_average):
    """
    This function returns True if the latest stock price is less
    than it's weekly average.
    """
    if stock_price < weekly_average:
        return True
    
def main():
    """
    The main function triggers the functions above then
    communicates with IFTTT by posting a request to trigger 
    an email to the assigned Gmail accounts with the IFTTT
    """
    api_key = "nmSjoGFt5z5ExJ4bLUMBcr0JozQykoHC2TB5dUNdUT4"     # my api key for authentication
    event_name = "stock_update"  # needed for my IFTTT trigger
    url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{api_key}"  # the api

    TICKER_LIST = ["AAPL","TSLA","MSFT","GOOGL","NKE"]  # symbol list stakeholder queried 
    weekly_avgs = store_weekly_avgs(TICKER_LIST) 
    json_file = "real_time_stock_data"  # name of json file 
    recent_stock_prices = []

    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            for key,value in data.items():
                recent_stock_prices.append([value][0])
            for i in range(len(weekly_avgs)):
                if latest_stock_lt_week_avg(recent_stock_prices[i],weekly_avgs[i]):
                    message = f"The stock price for {key} are less than 
                            the stock's weekly average. Buy more stocks now!!!"
                    data = {
                        'Value1':message
                    }
                    response = requests.post(url, json=data)
                    if response.status_code == 200:
                        print("Email sent!")
                    else:
                        print("Failed to send email.")
                        print("And yes, there has been a drop of prices")

    except FileNotFoundError:
        print(f"The file '{json_file}' was not found.")
    except json.JSONDecodeError:
        print(f"The file '{json_file}' is not a valid JSON file.")
    

