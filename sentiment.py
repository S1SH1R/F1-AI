from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import pandas as pd
import bs4 as bs
import requests


def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment = sid.polarity_scores(text)
    return sentiment['compound']

def fetch_sentiment_data(url):
    # Send a request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to retrieve data")
        return pd.DataFrame()

    # Parse the content of the request with BeautifulSoup
    soup = bs(response.content, 'html.parser')

    # Find elements containing news headlines - adjust this according to the website's structure
    headlines = soup.find_all('h2', class_='news-headline')

    # Extract the text from each headline element
    articles = [{'date': '2023-11-23', 'headline': headline.text.strip()} for headline in headlines]

    # Convert to DataFrame
    return pd.DataFrame(articles)

# Example sentiment data fetching and processing
sentiment_df = fetch_sentiment_data("https://finance.yahoo.com/news/p-500-trade-near-time-181928431.html") # You need to implement this
print(sentiment_df)

sentiment_df['sentiment_score'] = sentiment_df.apply(analyze_sentiment)
daily_sentiment = sentiment_df.groupby('date')['sentiment_score'].mean().reset_index()

