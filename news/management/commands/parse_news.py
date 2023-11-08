from django.core.management.base import BaseCommand
from . import *
from news.models import News
import requests

def translate_text(data):
    url = "https://nlp-translation.p.rapidapi.com/v1/translate"

    querystring = {"text":f"{data[0]} | {data[1]} | {data[2]} |","to":"uk","from":"en"}

    headers = {
        "X-RapidAPI-Key": TRANSLATE_API_KEY,
        "X-RapidAPI-Host": TRANSLATE_API_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    result = {}
    temp_word = ""
    k = 0
    for i in response.json()['translated_text']['uk']:
        if i == "|":
            k+=1
            result[f'key_{k}'] = temp_word
            temp_word = ""
            continue
        temp_word += i
    return result
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
                        text_translate = translate_text([title, description, content])
                        if news['creator']: 
                            News.objects.create(
                                title = text_translate[0], 
                                author = news['creator'],
                                link = news['link'],
                                image_url = news['image_url'],
                                pub_date = news['pubDate'],
                                description = text_translate[1],
                                country = news['country'],
                                content = text_translate[2]
                            )
                        else:
                            News.objects.create(
                                title = text_translate[0], 
                                link = news['link'],
                                image_url = news['image_url'],
                                pub_date = news['pubDate'],
                                description = text_translate[1],
                                country = news['country'],
                                content = text_translate[2]
                            )
                    except Exception as e:
                        print(e)
                        continue
                else:
                    print(data)
        except Exception as e:
            print(f'Error: {e}')