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

try:
    API_KEY = TranslationKeys.objects.filter(active=True).first()
    if API_KEY is None:
        raise ValueError("Активных ключей нету")
except ValueError as e:
    print(e)
    try:
        API_KEY = TranslationKeys.objects.filter(characters_translate__lt=300000).first()
        if API_KEY is None:
            raise ValueError("Ключей, которые имеют неиспользованный лимит по символам, нету")
    except ValueError as e:
        raise RuntimeError("Не удалось найти подходящий ключ")


def translate_content(data):
    if check_characters_translate_limit(len(data), API_KEY.characters_translate):
        change_api_key_for_translate()
    url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"
    headers = {
        "X-RapidAPI-Key": str(API_KEY.key),
        "X-RapidAPI-Host": API_HOST,
        "Content-Type": "application/json"
    }
    i = 0
    requests_counter = 0
    translated_content = ""
    if len(data) > 1000:
        while i < len(data):
            payload = {"q": f"{data[i:i+1000]}", "source": "en", "target": "uk"}
            response = requests.post(url, headers=headers, json=payload)
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
        return translated_content
    else:
        payload = {"q": f"{data[i:i+1000]}", "source": "en", "target": "uk"}
        response = requests.post(url, headers=headers, json=payload)
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
        return translated_content


def check_characters_translate_limit(text_length: int, key_translate_characters:int):
    if key_translate_characters + text_length >= 300000:
        return True
    else:
        return False


def change_api_key_for_translate():
    global API_KEY
    with transaction.atomic():
        API_KEY.active = False
        API_KEY.characters_translate = 300000
        API_KEY.save()

        try:
            API_KEY = TranslationKeys.objects.filter(active=True).first()
            if API_KEY is None:
                raise ValueError("Активных ключей нету")
        except ValueError as e:
            print(e)
            try:
                API_KEY = TranslationKeys.objects.filter(characters_translate__lt=300000).first()
                if API_KEY is None:
                    raise ValueError("Ключей, которые имеют неиспользованный лимит по символам, нету")
            except ValueError as e:
                raise RuntimeError("Не удалось найти подходящий ключ")


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
            news_author, _ = Author.objects.get_or_create(name="Команда Simple IT News")
            News.objects.filter(title=chosen_news.title).update(author = news_author)