import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def fetch_news(company, num_articles = 10):
    """ Fetch recent news articles about a company from NewsAPI
    """
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': company,
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': num_articles,
        'apiKey': NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get('status') != 'ok':
        raise Exception(f'NewsAPI error: {data.get('message')}') 
    
    articles = []
    for article in data.get('articles', []):
        if article.get('content') and article.get('title'):
            articles.append({
                'title': article['title'],
                'content': article['content'],
                'url': article['url'],
                'publishedAt': article['publishedAt'],
                'source': article['source']['name']
            })

    return articles