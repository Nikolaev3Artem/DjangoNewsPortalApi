from django.db import models
from admin_extra_buttons.api import button, confirm_action
from django.contrib import admin

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
    IsAproved = models.BooleanField(default=False)
    
    @button(html_attrs={'style': 'background-color:#DC6C6C;color:red'})
    def confirm(self, request):
        def _action(request):
            IsAproved = True

        return confirm_action(self, request, _action, "Confirm action",
                          "Successfully executed", )
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

@admin.action(description="Publish post")
def make_published(modeladmin, request, queryset):
    queryset.update(IsAproved=True)

class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", 'country', "IsAproved"]
    ordering = ["IsAproved"]
    actions = [make_published]