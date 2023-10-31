from django.db import models

# Create your models here.
class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50, default="Site Admin")
    link = models.CharField(max_length=200)
    image_url = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    pub_date =  models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)

    def __str__(self):
        return self.title