from django.core.management.base import BaseCommand
from . import *
from news.models import News
import requests

class Command(BaseCommand):
    help = 'Parsing news from newsdata.io'

    def handle(self, *args, **options):
        try:
            url = f'https://newsdata.io/api/1/news?apikey={api_key}&category=technology&language=en'
            response = requests.get(url)
            data = response.json()
            for news in data['results']:
                if news != "message":
                    try:
                        if news['creator']: 
                            News.objects.create(
                                title = news['title'], 
                                author = news['creator'],
                                link = news['link'],
                                image_url = news['image_url'],
                                pub_date = news['pubDate'],
                                description = news['description'],
                                country = news['country'],
                                content = news['content']
                            )
                        else:
                            News.objects.create(
                                title = news['title'], 
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
                else:
                    print(data)
        except Exception as e:
            print(f'Error: {e}')