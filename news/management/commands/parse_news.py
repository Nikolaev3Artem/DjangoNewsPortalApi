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
                        # print(f"Image Url: {news['image_url']} \n\
                        #     Content: {news['content']} \n\
                        #     Creator: {news['creator']} \n\
                        #     Pub Date: {news['pubDate']} \n\
                        #     Description: {news['description']} \n\
                        #     Country: {news['country']}\n\n\n")
                        
                        if news['image_url'] and \
                            len(news['content']) != 0 and \
                            news['pubDate'] and \
                            news['description'] and \
                            news['country'] and \
                            news['image_url'][0:4] == 'https':
                            if len(news['content']) >= 1800:
                                content = news['content'][0:1800]
                            else:
                                content = news['content']
                            
                            creators = news['creator']
                            if news['creator']: 
                                News.objects.create(
                                    title = news['title'], 
                                    link = news['link'],
                                    news_creator = creators,
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
        
