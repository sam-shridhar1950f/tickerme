import os
from dotenv import load_dotenv
import yfinance as yf
from twilio.rest import Client

load_dotenv()

def check_price(ticker, target_price):
    try:

        ticker = yf.Ticker(ticker)
        todays_data = ticker.history(period='1d')
        current_price = todays_data['Close'][0]
        
        if current_price is None:
            print(f"Error: Could not fetch price for {ticker}")
            return None
        print(current_price)
        return current_price <= target_price
    except Exception as e:
        print(f"Error checking price for {ticker}: {str(e)}")
        return None

def send_sms(message):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_phone = os.getenv('TWILIO_FROM_PHONE')
    to_phone = os.getenv('TWILIO_TO_PHONE')
    
    if not all([account_sid, auth_token, from_phone, to_phone]):
        print("Error: Missing Twilio credentials in environment variables")
        return
        
    client = Client(account_sid, auth_token)
    
    client.messages.create(
        body=message,
        from_=from_phone,
        to=to_phone
    )

def main():
    ticker = 'TSLA'  # Example
    target_price = 407
    
    result = check_price(ticker, target_price)
    if result is None:
        message = f"Failed to check price for {ticker}"
    elif result:
        message = f"{ticker} has hit target price of ${target_price}"
    else:
        # message = f"{ticker} has not hit target price of ${target_price}"
        pass
    send_sms(message)

main()