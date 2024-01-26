from django.core.management.base import BaseCommand
from news.models import News
class Command(BaseCommand):
    help = 'deleting all not posted news from database'
    
    def handle(self, *args, **options):
        news = News.objects.filter(is_approved=False)
        for i in news:
            i.delete()