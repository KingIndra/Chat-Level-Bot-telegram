import requests
from collections import deque

API_KEY = '800535f67fb24dee929821f87bd06d65'
NEWS_API_URL = f'https://newsapi.org/v2/top-headlines'

class FetchNews:

    def __init__(self):
        self.key = API_KEY
        self.queues = {}


    def news(self, country='in', category='entertainment', pageSize = 99):
        queue = self.queues.get((country, category))
        if not queue:
            self.queues[(country, category)] = self.fetch_news(country, category, pageSize)
            return self.news()
        else:
            if len(queue) == 0:
                self.queues[(country, category)] = self.fetch_news(country, category, pageSize)
                self.news()
            news_obj =  self.queues[(country, category)].popleft()
            return news_obj['title']
        
    
    def fetch_news(self, country='in', category='entertainment', pageSize = 99):

        parameters = {
            'country': country,        
            'pageSize': pageSize,          
            'apiKey': self.key,
            'category': category,
        }

        try:
            response = requests.get(NEWS_API_URL, params=parameters)
            response_data = response.json()
            if response_data['status'] == 'ok':
                articles = response_data['articles']
                queue = deque()
                for index, article in enumerate(articles, 1):
                    title = article['title']
                    description = article['description']
                    url = article['url']
                    new_obj = {
                        'title': title,
                        'description': description,
                        'url': url
                    }
                    queue.append(new_obj)
                return queue 
            else:
                return "Error fetching news: " + response_data['message']

        except requests.exceptions.RequestException as e:
            return "Error fetching news: " + e