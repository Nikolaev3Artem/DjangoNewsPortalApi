from django.core.management.base import BaseCommand
from news.models import News
import requests
import os
from dotenv import load_dotenv
import requests
load_dotenv()

def text_to_time(text):
    word_count = 0
    for word in text:
        if word != ' ':
            word_count += 1
    
    return int(word_count/238)

class Command(BaseCommand):
    help = 'Parsing news from newsdata.io'
    API_KEY = os.getenv('NEWS_API_KEY')
    def handle(self, *args, **options):
        try:                
            url = f'https://newsdata.io/api/1/news?apikey={self.API_KEY}&category=technology&language=en'
            response = requests.get(url)
            data = response.json()
            for news in data['results']:
                if news == "message":
                    raise Exception('Invalid data: ' . json.dumps(data, indent=4))
                
                if news['image_url'] and \
                    len(news['content']) != 0 and \
                    news['pubDate'] and \
                    news['description'] and \
                    news['country'] and \
                    news['image_url'][0:5] == 'https':
                    # print(f" \
                    #     Link: {news['link']} \n\
                    #     Title: {news['title']} \n\
                    #     Image Url: {news['image_url']} \n\
                    #     Content: {news['content']} \n\
                    #     Creator: {news['creator']} \n\
                    #     Pub Date: {news['pubDate']} \n\
                    #     Description: {news['description']} \n\
                    #     Country: {news['country']}\n\n\n")
                        
                    if news['creator']:
                        creators = ""
                        for creator in news['creator']:
                            creator += creators
                    else:
                        creators = news['creator']

                    News.objects.create(
                        title = news['title'], 
                        link = news['link'],
                        news_creator = creators,
                        image_url = news['image_url'],
                        pub_date = news['pubDate'],
                        update_date = news['pubDate'],
                        description = news['description'],
                        country = news['country'],
                        content = news['content'],
                        time_to_read = text_to_time(news['content'])
                    )                     
        except Exception as e:
            print(f'Error: {e}')
        
