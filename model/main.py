import nltk
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from summa import summarizer
import re
from nltk.tokenize import word_tokenize
import requests
from bs4 import BeautifulSoup
from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax
import torch
import ollama
from rake_nltk import Rake


nltk.download('punkt')
nltk.download('stopwords')

def extract_articles_from_website(url):
    sentiment_words = []  # Initialize sentiment_words with an empty list
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', class_='native_story')
        if articles:
            for article in articles:
                title_element = article.find('h1', class_='native_story_title')
                title = title_element.text.strip() if title_element else "Title not found"
                url_element = article.find('input', class_='native_story_url')
                url = url_element['value'] if url_element else "URL not found"
                synopsis_element = article.find('h2', class_='synopsis')
                synopsis = synopsis_element.text.strip() if synopsis_element else "Synopsis not found"
                print("Title:", title)
                print("URL:", url)
                print("Synopsis:", synopsis)
                print("-" * 50)

        content_divs = soup.find_all('div', class_='container')
        for content_div in content_divs:
            content = content_div.find('div', class_='full-details')
            if content:
                content_text = content.get_text(strip=True)
                print("Content from second div:")
                print(content_text)
                print("-" * 50)

                sentiment_analyzer = SentimentIntensityAnalyzer()
                sentiment_scores = sentiment_analyzer.polarity_scores(content_text)
                print("Sentiment Analysis Results:")
                for key, value in sentiment_scores.items():
                    print(f"{key}: {value}")

                print("\nSentiment-related words:")
                if sentiment_scores['compound'] < -0.5:  # If compound score is highly negative
                    words = nltk.word_tokenize(content_text.lower())
                    stop_words = set(stopwords.words('english'))
                    sentiment_words = [word for word in words if word not in stop_words and word.isalpha() and len(word) > 2]
                    print(sentiment_words)
                else:
                    print("Compound score not highly negative.")

                break
        if not content:
            print("No articles found in the second div.")
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)
    return content_text, sentiment_words


url = "https://indianexpress.com/article/cities/bangalore/electoral-bonds-raise-questions-about-rule-by-the-people-says-prashant-bhushan-9284970/#:~:text=%E2%80%9CThe%20limit%20was%20Rs%2075,the%20last%20six%20years%E2%80%A6.."
content_text, sentiment_words = extract_articles_from_website(url)