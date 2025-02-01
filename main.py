import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os
load_dotenv()
from_=os.getenv('from_')
account_sid=os.getenv('account_sid')
auth_token=os.getenv('auth_token')
to=os.getenv('to_addr')

stock_api_key=os.getenv('stock_api_key')
stock_url="https://www.alphavantage.co/query"
news_api_key=os.getenv('news_api_key')
news_url="https://newsapi.org/v2/everything"
company_name="TSLA"
function_type="TIME_SERIES_DAILY"
parameters={
    "function":function_type,
    "symbol":company_name,
    "apikey":stock_api_key
}
news_params={
    "q":company_name,
    "apiKey":news_api_key
}

response1=requests.get(stock_url,params=parameters)
response1.raise_for_status()
data=response1.json()

response2=requests.get(news_url,params=news_params)
response2.raise_for_status()
news_data=response2.json()['articles']
three_articles=news_data[:3]


yesterday=data['Time Series (Daily)']['2024-12-20']
yesterdays_closing_price = yesterday['4. close']

day_before_yesterday=data['Time Series (Daily)']['2024-12-19']
day_before_yesterdays_closing_price = day_before_yesterday['4. close']


difference=float(yesterdays_closing_price )-float(day_before_yesterdays_closing_price )
if difference>0:
    up_stock="👍"
else:
    up_stock="👎"

stock_percen=round((difference / float(yesterdays_closing_price)) *100)
formatted_articles=[f"Headlines:{article['title']} {company_name}{up_stock} , \n Brief:{article['description']}" for article  in  three_articles]
client = Client(account_sid, auth_token)
if abs(stock_percen ) > 3:
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=from_,
            to=to
        )

