from django.core.management.base import BaseCommand
import requests
import os
from news.models import News, TranslationKeys, Categories, Author
import datetime
import random

from dotenv import load_dotenv
import requests
load_dotenv()
# key = TranslationKeys.objects.get(active=True)
# key.requests = 302
# key.save(['requests'])
API_HOST = os.getenv('TRANSLATE_API_HOST')
API_KEY = TranslationKeys.objects.filter(active=True)

if TranslationKeys.objects.get(active=True).requests >= 300:
    API_KEY.update(active=False)

if str(datetime.datetime.now())[8:10] == 00:
    TranslationKeys.objects.all().update(requests=0)
    
def translate_content(data):
    url = "https://nlp-translation.p.rapidapi.com/v1/translate"
    headers = {"X-RapidAPI-Key": API_KEY[0].key,
            "X-RapidAPI-Host": API_HOST}
    i = 0
    requests_counter = 0
    translated_content = ""
    
    while i < len(data):
        querystring = {"text": f"{data[i:i+1000]}", "to": "uk", "from": "en"}
        response = requests.get(url, headers=headers, params=querystring)
        translated_content += response.json()['translated_text']['uk']
        i += 1000
        requests_counter += 1
    requests_counter += API_KEY[0].requests
    API_KEY.update(requests = requests_counter)

    return translated_content
 
def translate_text(data):
    url = "https://nlp-translation.p.rapidapi.com/v1/translate"
    if len(data) == 2:  
        querystring = {
            "text": f"{data[0]} | {data[1]} |", "to": "uk", "from": "en"}
    else:
        querystring = {"text": f"{data[0]} |", "to": "uk", "from": "en"}
    headers = {"X-RapidAPI-Key": API_KEY[0].key,
            "X-RapidAPI-Host": API_HOST}
    response = requests.get(url, headers=headers, params=querystring)
    
    requests_counter = 0
    requests_counter += API_KEY[0].requests
    API_KEY.update(requests = requests_counter)
    result = {}
    temp_word = ""
    k = 0
    for i in response.json()['translated_text']['uk']:
        if i == "|":
            k += 1
            result[f'key_{k}'] = temp_word
            temp_word = ""
            continue
        temp_word += i
    return result

class Command(BaseCommand):
    help = 'Translating parsed news'
    
    def handle(self, *args, **options):
        news = News.objects.all().filter(pub_date__gte = f'{str(datetime.datetime.now())[0:10]}T00:00:00', pub_date__lte = f'{str(datetime.datetime.now())[0:10]}T23:59:59', translated=False)
        print(news)
<<<<<<< HEAD
        print(f'{str(datetime.datetime.now())[0:9]} 00:00:00')
        print(f'{str(datetime.datetime.now())[0:9]} 23:59:59')
=======
  
>>>>>>> 1fa908f (123)
        for i in range(0,3):
            print(f'i: {i}')
            if len(news) != 0:
                chosen_news = random.choice(news)
                print(f"Chosen news: {chosen_news}")
                chosen_news.custom_url = ' '.join(chosen_news.title.split(' ')[0:4])

                temp_url = ''
                for var in chosen_news.custom_url:
                    if var.isalnum() or var == '-':
                        temp_url += var
                chosen_news.custom_url = temp_url.lower().replace(' ','-')

                # translate = translate_text([chosen_news.title, chosen_news.description])
                # chosen_news.title = translate['key_1']
                # chosen_news.description = translate['key_2']
                # chosen_news.content = translate_content(chosen_news.content)
                chosen_news.translated = True
                chosen_news.is_approved = True
                chosen_news.save()
                news_category = Categories.objects.get(title="news").id
                chosen_news.categories.add(news_category)

                news_author = Author.objects.get(name="Команда Simple IT News")
                News.objects.all().filter(title=chosen_news.title).update(author = news_author)
                print(chosen_news)
