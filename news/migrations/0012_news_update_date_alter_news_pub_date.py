

from django.db import migrations, models

def migrate_old_data(apps, schema_editor):
    News = apps.get_model('news', 'news')
    for news in News.objects.all():
        news.update_date = news.pub_date
        news.save(update_fields=["update_date"])

class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_alter_news_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='update_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='pub_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.RunPython(migrate_old_data, reverse_code=migrations.RunPython.noop),
    ]
