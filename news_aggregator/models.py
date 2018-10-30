from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=80)

    def __str__(self):
        return f"Tag {self.tag_id}: {self.tag_name}"

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

class Resource(models.Model):
    resource_url = models.URLField(primary_key=True)
    country = models.CharField(max_length=120)

    def __str__(self):
        return f"Resource: {self.resource_url}"

    class Meta:
        verbose_name = 'resource'
        verbose_name_plural = 'resources'


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    content = models.TextField(blank=False)
    category = models.CharField(max_length=120)
    publication_date = models.DateTimeField(auto_now=True)
    tag_id = models.ManyToManyField(Tag, through='news_tag')

    def __str__(self):
        return f"{self.news_id}: {self.title}"

    class Meta:
        verbose_name = 'news'
        verbose_name_plural = 'news'


class news_resource(models.Model):
    id = models.AutoField(primary_key=True)
    news_id = models.ForeignKey(News, on_delete=models.SET_NULL, null=True, to_field='news_id')
    resource_url = models.ForeignKey(Resource, on_delete=models.SET_NULL, null=True, to_field='resource_url')

class news_tag(models.Model):
    id = models.AutoField(primary_key=True)
    news_id = models.ForeignKey(News, on_delete=models.SET_NULL, null=True, to_field='news_id')
    tag_id = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, to_field='tag_id')

    def __str__(self):
        return f"{self.id}: news_id {self.news_id} to tag_id {self.tag_id}"