# First things first
1. "AAPL", "MSFT", "GOOGL", "TSLA", "NKE" and 0.25 are default settings for companies and drop level. You can change those at your own discretion.  
2. Create .env file locating it in your current working directory
3. Make sure .gitignore has .env
4. Inside .env set your email details: 

EMAIL_USER=here_is_your_gmail_account@gmail.com
RECEIVER_EMAIL=here_is_your_gmail_account@gmail.com
EMAIL_PASS=here past your pass (see below)

5. Proceed with adding password inside .env following the procedure below

# Create & use app passwords

To help keep your account secure, use "Sign in with Google" to connect apps to your Google Account

1. Go to your Google Account.
2. Select Security.
3. Under "How you sign in to Google," select 2-Step Verification.
4. At the bottom of the page, select App passwords.
5. Enter a name that helps you remember where you’ll use the app password.
6. Select Generate and follow the instructions on your screen. The app password is the 16-character code that generates on your device.

Paste it in .env file replacing here past your pass with whatever 16-character you got:

EMAIL_PASS=here past your pass

# Stock exchange working hours
Our example is looking at "AAPL", "MSFT", "GOOGL", "TSLA", "NKE", which are listed in US. Since stock exchange is not trading 24/7, our watcher will see no change during closed time. 
You could replace the tickers with any other companies listed at Stock Exchanges located in working time zones, just double-check at Yahoo finance the ticker is correct.


# Why smtplib over IFTTT
Following YAGNI principle we believe the requirement of sending notification via email provides exactly what we need. For this task smtplib offers more direct and controllable solution, also it is free.

Considering further versions, IFTTT would be chosen for additional web notification solutions, such as Facebook, Telegram, SMS etc. 

# Why yfinance over API
yfinance is a library for fetching market data from Yahoo Finance. It provides a simpler interface for fetching stock data compared to making HTTP requests to an API, parsing the responses, and handling errors. 

Given that we are planning to run the script every minute, this would total to a max of 1,440 requests per day (assuming one request per run). This falls well within the documented rate limits for the public API based on IP address (48,000 requests per day)

# Create & use app passwords

To help keep your account secure, use "Sign in with Google" to connect apps to your Google Account

1. Go to your Google Account.
2. Select Security.
3. Under "Signing in to Google," select 2-Step Verification.
4. At the bottom of the page, select App passwords.
5. Enter a name that helps you remember where you’ll use the app password.
6. Select Generate and follow the instructions on your screen. The app password is the 16-character code that generates on your device.

Paste it in .env file replacing here past your pass with whatever 16-character you got:
EMAIL_PASS=here past your pass

"AAPL", "MSFT", "GOOGL", "TSLA", "NKE"