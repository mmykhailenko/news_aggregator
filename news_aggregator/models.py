from datetime import timezone

from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField()
    resource = models.CharField(max_length=200)
    category = models.CharField(max_length=200)


    def __str__(self):
        return self.title

