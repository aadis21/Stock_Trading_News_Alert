import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "+18596462741",
VERIFIED_NUMBER = "+917717667030",

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "NCOIG2EBZZWQ8M96"
NEWS_API_KEY = "48a19d3d53954dbcbfed7b0edd056902"
TWILIO_SID = "AC7926ff70196e06875eeedc8209325329"
TWILIO_AUTH_TOKEN = "222865ef669fa3d199c1fad8995b5bba"

##https://www.alphavantage.co/documentation/#daily


#Get yesterday's closing stock price
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]



#Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]


#Find the positive difference between 1 and 2. e.g. 40 - 20 = -20
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(yesterday_closing_price)) * 100)

#If difference percentage is greater than 5 then print("Get News").
if abs(diff_percent) >= 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,

    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]


    #Use Python slice operator to create a list that contains the first 3 articles.
    three_articles = articles[:3]


    ##Use Twilio to send a seperate message with each article's title and description to your phone number.

    #Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    
    #Send each article as a separate message via Twilio.
    client = Client("AC7926ff70196e06875eeedc8209325329","222865ef669fa3d199c1fad8995b5bba",)

    #Send each article as a separate message via Twilio.
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+18596462741",
            to="+917717667030",
        )
