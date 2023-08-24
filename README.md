# API-Stock-Signalling

This Python application monitors real-time stock prices and notifies users when specific conditions are met:

1. When the stock price falls by at least $0.25 USD.
2. When today's stock price is less than the 7-day average.

## Prerequisites

- Python 3.x
- An API key from Financial Modeling Prep (FMP)
- IFTTT account and key for notifications

## Getting Started

### Step 1: Get Your FMP API Key

1. Visit [Financial Modeling Prep](https://site.financialmodelingprep.com) website.
2. Sign up for an account and generate your API key.

### Step 2: Set Up Your `.env` File

1. Create a new file in the root directory of your project and name it `.env`.
2. Open `.env` and add the following lines:

   ```
   API_KEY=Your_FMP_API_Key_Here
   WEBHOOK_KEY=Your_IFTTT_Key_Here
   ```

### Step 3: Get Your IFTTT Key

1. Visit the [IFTTT website](https://ifttt.com/) and create an account if you don't have one.
2. Generate your IFTTT key.

### Step 4: Create an IFTTT Applet

1. Log in to your IFTTT account.
2. Create a new applet.
3. Set the event name to `stock_price_fell`.
4. Configure the applet to receive notifications when this event is triggered.

### Step 5: Install Required Python Packages

If you haven't done so already, install the required Python packages by running:

```bash
pip install -r requirements.txt

```
