from django.core.management.base import BaseCommand, CommandError
import requests
import os
from news.models import News

api_key = os.getenv('NEWS_API_KEY')

class Command(BaseCommand):
    help = "Parsing news using API"

    def handle(self, *args, **options):
        try:
            url = f'https://newsdata.io/api/1/news?apikey={api_key}&category=technology'
            response = requests.get(url)
            data = response.json()
            for news in data['results']:
                print(news)
                try:
                    News.objects.create(
                        news_id = news['article_id'], 
                        title = news['title'], 
                        author = news['creator'],
                        link = news['link'],
                        image_url = news['image_url'],
                        pub_date = news['pubDate'],
                        description = news['description'],
                        country = news['country'],
                        content = news['content']
                    )
                except Exception as e:
                    print(e)
                    continue
            print('All done news are parsed!')
        except Exception as e:
            print(f'Error: {e}')