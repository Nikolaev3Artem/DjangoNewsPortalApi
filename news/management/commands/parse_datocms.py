from django.core.management.base import BaseCommand
from . import *
from news.models import Author
import requests
from dotenv import load_dotenv
import os
load_dotenv()

def parse_authors():
    url = 'https://graphql.datocms.com/'
    query = '''
        {
            allAuthors {
                id
                route
                socials
                authorname
                authordescription
            }
        }
    '''
    headers = {"Authorization":os.getenv('BEARER_DATOCMS')}
    json_data = {
        "query": query,
        }
    request = requests.post(url=url, json=json_data,headers=headers)
    responce = request
    authors = Author.objects.all()
    if responce.status_code == 200:
        for author in responce.json()['data']['allAuthors']:
            create_new_author = True
            twitter = None
            telegram = None
            facebook = None
            if 'twitter' in author["socials"].keys():
                twitter =  author["socials"]["twitter"]
            elif 'telegram' in author["socials"].keys():
                telegram =  author["socials"]["telegram"]
            elif 'facebook' in author["socials"].keys():
                facebook =  author["socials"]["facebook"]
            
            for our_author in authors:
                if author['authorname'] == our_author.name:
                    create_new_author = False
            if create_new_author:
                Author.objects.create(
                    name = author['authorname'],
                    route = author["route"],
                    twitter = twitter,
                    telegram = telegram,
                    facebook = facebook,
                    description = author["authordescription"]
                )
def parse_tags():
    ...

def parse_all():
    parse_authors()
    parse_tags()
    return 200

class Command(BaseCommand):


    help = 'Parsing authors and tags from datocms'

    def handle(self, *args, **options):
        if options['authors']:
            parse_authors()
        elif options['tags']:
            parse_tags()
        elif options['all']:
            parse_all()

    def add_arguments(self, parser):
        parser.add_argument(
            "-A",
            "--authors",
            action='store_true',
            default=False,
            help="Parsing authors from datocms",
        )
        parser.add_argument(
            "-T",
            "--tags",
            action='store_true',
            default=False,
            help="Parsing tags from datocms",
        )
        parser.add_argument(
            "--all",
            action='store_true',
            default=False,
            help="Parsing all info that we need from datocms",
        )

        
