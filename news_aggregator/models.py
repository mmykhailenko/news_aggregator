from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Resource(models.Model):

    resource_url = models.CharField(max_length=100, primary_key=True)
    location = models.CharField(max_length=50)

    def __str__(self):
        return "{}, {}".format(self.resource_url, self.location)


class News(models.Model):

    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tag = models.ManyToManyField(Tag)
    resource = models.ManyToManyField(Resource)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'news'

    def __str__(self):
        return self.title


class User(models.Model):

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    password = models.CharField(max_length=40)

    def __str__(self):
        return "{} {}".format(self.first_name,  self.last_name)
