from django.db import models

# Create your models here.



class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    categories = models.CharField(max_length=100,default='X')
    announcer = models.CharField(max_length=100, null=False,default='X')