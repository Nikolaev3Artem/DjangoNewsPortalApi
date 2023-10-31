
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('news_id', models.CharField(max_length=150)),
                ('title', models.CharField(max_length=50)),
                ('author', models.CharField(default='Site Admin', max_length=50)),
                ('link', models.CharField(max_length=200)),
                ('image_url', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=1000)),
                ('pub_date', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=1000)),
            ],
        ),
    ]
