from django.core.management.base import BaseCommand
from django.db import transaction
import requests
import os
from news.models import News, TranslationKeys, Categories, Author
import datetime
import random

from dotenv import load_dotenv
import requests
load_dotenv()

API_HOST = os.getenv('TRANSLATE_API_HOST')

API_KEY = TranslationKeys.objects.filter(active=True).first()
if str(datetime.datetime.now())[8:10] == 00:
    TranslationKeys.objects.all().update(requests=0)


def translate_content(data):
    print("key = ", API_KEY.key)
    print("len data = ", len(data))
    check_characters_translate_limit(len(data))
    url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"
    headers = {
        "X-RapidAPI-Key": str(API_KEY.key),
        "X-RapidAPI-Host": API_HOST,
        "Content-Type": "application/json"
    }
    i = 0
    requests_counter = 0
    translated_content = ""
    print("translated characters in key =", API_KEY.characters_translate)
    if len(data) > 1000:
        while i < len(data):
            payload = {"q": f"{data[i:i+1000]}", "source": "en", "target": "uk"}
            response = requests.post(url, headers=headers, json=payload)
            print(response.json())
            if response.status_code == 200:
                words_count = len(data[i:i+1000])
                API_KEY.characters_translate += words_count
                translated_content += response.json()['data']['translations']['translatedText']
                i += 1000
                requests_counter += 1
            elif response.status_code == 403:
                API_KEY.active = False
                break
            elif response.status_code == 429:
                API_KEY.active = False
                API_KEY.characters_translate = 300000
                break
        requests_counter += API_KEY.requests
        API_KEY.requests = requests_counter
        API_KEY.save()
        print("translated characters in key =", API_KEY.characters_translate)
        return translated_content
    else:
        payload = {"q": f"{data[i:i+1000]}", "source": "en", "target": "uk"}
        response = requests.post(url, headers=headers, json=payload)
        print(response.json())
        if response.status_code == 200:
            words_count = len(data[i:i+1000])
            API_KEY.characters_translate += words_count
            translated_content += response.json()['data']['translations']['translatedText']
            requests_counter += 1
        elif response.status_code == 403:
            API_KEY.active = False
        elif response.status_code == 429:
            API_KEY.active = False
            API_KEY.characters_translate = 300000
        requests_counter += API_KEY.requests
        API_KEY.requests = requests_counter
        API_KEY.save()
        print("translated characters in key =", API_KEY.characters_translate)
        return translated_content



def check_characters_translate_limit(text_length):
    global API_KEY

    if API_KEY.characters_translate + text_length >= 300000:
        with transaction.atomic():
            API_KEY.active = False
            API_KEY.characters_translate = 300000
            API_KEY.save()

            API_KEY = TranslationKeys.objects.filter(active=True).first()
            if not API_KEY:
                raise Exception("Нет доступных ключей для перевода")
            else:
                print("new key = ", API_KEY.key)


class Command(BaseCommand):
    help = 'Translating parsed news'
    
    def handle(self, *args, **options):
        news = News.objects.all().filter(translated=False, is_approved=False, description__isnull=False)
        if len(news) != 0:
            chosen_news = random.choice(news)
            chosen_news.title = translate_content(chosen_news.title)
            chosen_news.description = translate_content(chosen_news.description)
            chosen_news.content = translate_content(chosen_news.content)
            chosen_news.translated = True
            chosen_news.is_approved = True
            chosen_news.save()
            news_category = Categories.objects.get(title="news").id
            chosen_news.categories.add(news_category)
            news_author = Author.objects.get(name="Команда Simple IT News")
            News.objects.all().filter(title=chosen_news.title).update(author = news_author)
