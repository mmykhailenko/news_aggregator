from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser):
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=80)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    content = models.TextField(blank=False)
    date = models.DateTimeField(auto_now=True)
    resource = models.URLField()
    category = models.ForeignKey('Category', on_delete=None)
    tag = models.ManyToManyField('Tag')

    def __str__(self):
        return f"{self.id}: {self.title}"

    class Meta:
        verbose_name = 'news'
        verbose_name_plural = 'news'


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)

    def __str__(self):
        return f"Category {self.id}: {self.name}"

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)

    def __str__(self):
        return f"Tag {self.id}: {self.name}"

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'