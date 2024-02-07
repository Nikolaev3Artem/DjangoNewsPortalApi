from django.core.management.base import BaseCommand
from aiogram import executor
import requests
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import os
from news.models import News
from asgiref.sync import sync_to_async
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
load_dotenv()

class Command(BaseCommand):
    help = 'Parsing news from newsdata.io'

    def handle(self, *args, **options):
        API_HOST = os.getenv('API_HOST')
        API_PORT = os.getenv('API_PORT')
        TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
        SIMPLE_IT_LINK = os.getenv('SIMPLE_IT_LINK')

        bot = Bot(token=str(os.getenv('BOT_TOKEN')))
        dp = Dispatcher(bot)
        sch = AsyncIOScheduler()

        print(f'Бот успішно запущенний!')

        async def on_shutdown(dp):
            await bot.close()

        async def forever_check():
            response = requests.get(f'{API_HOST}:{API_PORT}/api/ApprovedNews/social_posts')
            if response.status_code == 200:
                data = response.json()
                for news in data:
                    try:
                        await bot.send_photo(TELEGRAM_CHANNEL_ID, photo=news['image_url'], caption=f"""
    <b>{news['title']}</b>\n
    {news['description']}\n
    {SIMPLE_IT_LINK}/news/{news['custom_url']}""", parse_mode='HTML')
                        News.objects.filter(id = news['id']).update(already_posted=True)
                    except:
                        continue
                    
        sch.add_job(forever_check, "interval", seconds=7200)

        sch.start()
        executor.start_polling(dp)
