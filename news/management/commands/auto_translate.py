from django.core.management.base import BaseCommand
import requests
import os
from news.models import News, TranslationKeys, Categories, Author
import datetime
import random

from dotenv import load_dotenv
import requests
load_dotenv()

API_HOST = os.getenv('TRANSLATE_API_HOST')

API_KEY = TranslationKeys.objects.get(active=True)
if API_KEY.requests >= 300:
    API_KEY.active=False

if str(datetime.datetime.now())[8:10] == 00:
    TranslationKeys.objects.all().update(requests=0)
    
def translate_content(data):
    url = "https://nlp-translation.p.rapidapi.com/v1/translate"
    headers = {"X-RapidAPI-Key": str(API_KEY.key),
            "X-RapidAPI-Host": API_HOST}
    i = 0
    requests_counter = 0
    translated_content = ""
    
    if len(data) > 1000:
        while i < len(data):
            print(i)
            querystring = {"text": f"{data[i:i+1000]}", "to": "uk", "from": "en"}
            response = requests.get(url, headers=headers, params=querystring)
            if requests.status_codes == 200:
                translated_content += response.json()['translated_text']['uk']
                i += 1000
                requests_counter += 1
            elif response.status_code == 403:
                API_KEY.active = False
                break
            elif response.status_code == 429:
                API_KEY.active = False
                API_KEY.requests = 300
                break
        requests_counter += API_KEY.requests
        API_KEY.requests = requests_counter

        return translated_content
    else:
        querystring = {"text": f"{data[i:i+1000]}", "to": "uk", "from": "en"}
        response = requests.get(url, headers=headers, params=querystring)
        if requests.status_codes == 200:
            translated_content += response.json()['translated_text']['uk']
            requests_counter += 1
        elif response.status_code == 403:
            API_KEY.active = False
        elif response.status_code == 429:
            API_KEY.active = False
            API_KEY.requests = 300
        requests_counter += API_KEY.requests
        API_KEY.requests = requests_counter

        return translated_content
 
def translate_text(data):
    url = "https://nlp-translation.p.rapidapi.com/v1/translate"
    if len(data) == 2:  
        querystring = {
            "text": f"{data[0]} | {data[1]} |", "to": "uk", "from": "en"}
    else:
        querystring = {"text": f"{data[0]} |", "to": "uk", "from": "en"}
    headers = {"X-RapidAPI-Key": str(API_KEY.key),
            "X-RapidAPI-Host": API_HOST}
    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json())
    if response.status_code == 200:
        requests_counter = 0
        requests_counter += API_KEY.requests
        API_KEY.requests = requests_counter
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
    elif response.status_code == 403:
        API_KEY.active = False
    elif response.status_code == 429:
        API_KEY.active = False
        API_KEY.requests = 10
class Command(BaseCommand):
    help = 'Translating parsed news'
    
    def handle(self, *args, **options):
        news = News.objects.all().filter(translated=False, is_approved=False)
        if len(news) != 0:
            chosen_news = random.choice(news)
            translate = translate_text([chosen_news.title, chosen_news.description])
            chosen_news.title = translate['key_1']
            chosen_news.description = translate['key_2']
            chosen_news.content = translate_content(chosen_news.content)
            chosen_news.translated = True
            chosen_news.is_approved = True
            chosen_news.save()
            news_category = Categories.objects.get(title="news").id
            chosen_news.categories.add(news_category)
            news_author = Author.objects.get(name="Команда Simple IT News")
            News.objects.all().filter(title=chosen_news.title).update(author = news_author)