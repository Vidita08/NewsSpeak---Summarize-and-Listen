import requests
from datetime import datetime, timedelta

class NewsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"

    def get_company_news(self, company_name, days=7):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        params = {
            'q': company_name,
            'from': start_date.strftime('%Y-%m-%d'),
            'to': end_date.strftime('%Y-%m-%d'),
            'sortBy': 'publishedAt',
            'apiKey': self.api_key,
            'language': 'en'
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return None