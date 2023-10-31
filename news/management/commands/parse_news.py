from django.core.management.base import BaseCommand
from . import *
from news.models import News
class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        try:
            url = f'https://newsdata.io/api/1/news?apikey={api_key}&category=technology'
            response = requests.get(url)
            data = response.json()
            for news in data['results']:
                try:
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
                except Exception as e:
                    print(e)
                    continue
            print('All done news are parsed!')
        except Exception as e:
            print(f'Error: {e}')