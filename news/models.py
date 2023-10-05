from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=50)
    short_description = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    date =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title