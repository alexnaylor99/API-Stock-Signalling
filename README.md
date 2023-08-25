# Stock Price Alert System 📈

This project is designed to monitor stock prices of given symbols and alert via IFTTT if the stock price for a given day is significantly different from the average of the previous days.

## 📁 Files:

- **`main.py`**: This is the primary script which periodically fetches the stock prices for the symbols, calculates the average, and checks if an alert needs to be triggered.
- **`price_alert_utils.py`**: Contains utility functions to fetch stock prices and to send notifications to IFTTT.
- **`price_alert_utils_tests.py`**: Contains unit tests for the utility functions provided in `price_alert_utils.py`.
