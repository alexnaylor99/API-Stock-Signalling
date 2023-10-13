import unittest
import stock_signaller


class TestStockFunctions(unittest.TestCase):

    def test_get_exchange_rate(self):
        """
        Test if exchange rate function returns a float
        """
        result = stock_signaller.get_exchange_rate()
        self.assertIsInstance(result, float)

    def test_get_stock_price(self):
        """
        Test if immedate stock price function returns a float
        """
        result = stock_signaller.get_stock_price('AAPL', 1.5)
        self.assertIsInstance(result, float)

    def test_get_previous_stock_price(self):
        """
        Test if 1 minute prior stock price function returns a float
        """
        result = stock_signaller.get_previous_stock_price('AAPL', 1.5)
        self.assertIsInstance(result, float)

    def test_seven_day_average_return_type(self):
        """
        Test if seven-day stock price average function returns a float
         """
        result = stock_signaller.get_seven_day_average('AAPL', 1.5)
        self.assertIsInstance(result, float)

    def test_seven_day_average_calculation(self):
        """
        Test the calculation of the seven-day average
        """
        symbol = 'AAPL'
        exchange_rate = stock_signaller.get_exchange_rate()
        # personally calculating the expected seven-day average
        endpoint = (
            f"{stock_signaller.BASE_URL}/time_series?"
            f"symbol={symbol}&interval=1day&apikey={stock_signaller.API_KEY}"
        )
        response = stock_signaller.get(endpoint)
        data = response.json()
        last_seven_days = data['values'][:7]
        total = 0
        for day in last_seven_days:
            total += float(day['close']) * exchange_rate
        expected_average = total / 7
        # compare it with the returned value from the function
        result = stock_signaller.get_seven_day_average(symbol, exchange_rate)
        self.assertAlmostEqual(result, expected_average, places=2)

    def test_exchange_rate_multiplication(self):
        """
        Test the multiplication by the exchange rate
        """
        symbol = 'AAPL'
        exchange_rate = stock_signaller.get_exchange_rate()
        # get a stock price in USD
        usd_price = stock_signaller.get_stock_price(symbol, 1)
        # manually calculate expected value after exchange
        # rate multiplication
        expected_value = usd_price * exchange_rate
        # compare it with the returned value from the function
        result = stock_signaller.get_stock_price(symbol, exchange_rate)
        self.assertAlmostEqual(result, expected_value, places=2)




