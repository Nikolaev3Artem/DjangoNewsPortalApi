from django.core.management.base import BaseCommand
from news.models import News, Author, Categories
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

    def handle(self, *args, **options):
        GOOGLENEWS_API_KEY = os.getenv('GOOGLENEWS_API_KEY')
        GOOGLENEWS_API_HOST = os.getenv('GOOGLENEWS_API_HOST')
        url = "https://google-news-api1.p.rapidapi.com/search?language=en&q=technology"
        headers = {"X-RapidAPI-Key": '9e5b214306mshd2a6d5af8889f31p114a6fjsnf49014f3ad0a',
            "X-RapidAPI-Host": GOOGLENEWS_API_HOST}
        response = requests.get(url, headers=headers)
        
        # try:
        if response.status_code == 200:
            data = response.json()
            for news in data['news']['news']:
                if news['body'] is not None:
                    if len(news['body']) > 7000:
                        content = news['body'][0:7000]
                    else:
                        content = news['body']
                    try:
                        image = news['props']['image']
                    except:
                        image = ''
                    
                    news_author = Author.objects.get(name="Команда Simple IT News")
                    news_category = Categories.objects.get(title="news").id
                    # try:
                    temp_url = ''
                    for var in news['title'].split()[0:4]:
                        if var.isalnum() or var == '-':
                            temp_url += '-' + var 
                    custom_url = temp_url.lower().replace(' ','-')
                    news = News.objects.create(
                        title = news['title'],
                        link = news['link'],
                        author= news_author,
                        image_url = image,
                        pub_date = news['date'][0:19],
                        update_date = news['date'][0:19],
                        description = news['description'],
                        content = content,
                        time_to_read = text_to_time(content),
                        custom_url = custom_url[1:-1]
                    )
                    news.categories.add(news_category)
        else:
            print(response.json())

                # except:
                #     continue
        # except Exception as error:
        #     print(f"KeyError: {error}")