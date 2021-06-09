import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

ALPHA_API_KEY = "****************"
NEWS_API_KEY = "*****************"

STOCK_ENDPOINT = "********************"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

TWILIO_ACCOUNT_SID = "*******************"
TWILIO_AUTH_TOKEN = "*********************"


stock_params = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK_NAME,
    "interval": "15min",
    "apikey": ALPHA_API_KEY
}

alpha_response = requests.get(STOCK_ENDPOINT, params=stock_params)
alpha_response.raise_for_status()
raw_data = alpha_response.json()["Time Series (15min)"]

data_list = [value for (key, value) in raw_data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]


day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]


pos_diff = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
percent_diff = (float(pos_diff) / float(yesterday_closing_price)) * 100

if percent_diff > 0:
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]

    three_articles = news_data[:3]

    formatted_articles = [f"Headline {article['title']}. \nBrief: {article['description']}" for article in three_articles]


    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages \
            .create(
            body=article,
            from_='+14088344343',
            to='+12037154454'
        )


