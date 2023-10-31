from django.db import models

# Create your models here.
class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, default="none", null=True)
    author = models.CharField(max_length=50, default="Site Admin", null=True)
    link = models.CharField(max_length=200, default="none", null=True)
    image_url = models.CharField(max_length=500, default="none", null=True)
    description = models.CharField(max_length=1000, default="none", null=True)
    pub_date =  models.CharField(max_length=100, default="none", null=True)
    country = models.CharField(max_length=50, default="none", null=True)
    content = models.CharField(max_length=1000, default="none", null=True)

    def __str__(self):
        return self.title