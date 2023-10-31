from django.db import models

# Create your models here.
class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=True)
    author = models.CharField(max_length=50, default='SimpleITNews')
    link = models.CharField(max_length=200, null=True, unique=True)
    image_url = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=1000, null=True)
    pub_date =  models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=50, null=True)
    content = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "News"