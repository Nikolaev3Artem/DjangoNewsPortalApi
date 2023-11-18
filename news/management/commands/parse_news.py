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
                        if news['image_url'] != None or news['image_url'][0:4] == 'https' & len(news['content']) != 0:
                            if len(news['content']) >= 1800:
                                content = news['content'][0:1800]
                            else:
                                content = news['content']
                                
                            if news['creator']: 
                                News.objects.create(
                                    title = news['title'], 
                                    author = news['creator'],
                                    link = news['link'],
                                    image_url = news['image_url'],
                                    pub_date = news['pubDate'],
                                    update_date = news['pubDate'],
                                    description = news['description'],
                                    country = news['country'],
                                    content = content
                                )
                            else:
                                News.objects.create(
                                    title = news['title'], 
                                    link = news['link'],
                                    image_url = news['image_url'],
                                    pub_date = news['pubDate'],
                                    update_date = news['pubDate'],
                                    description = news['description'],
                                    country = news['country'],
                                    content = content
                                )                        
                    except Exception as e:
                        print(e)
                        continue
                else:
                    print(data)
        except Exception as e:
            print(f'Error: {e}')