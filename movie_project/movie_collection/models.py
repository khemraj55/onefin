from django.db import models

# Create your models here.
from django.db import models
from uuid import uuid4


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    genres = models.CharField(max_length=255, blank=True)
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    def __str__(self):
        return self.title

class Collection(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    movies = models.ManyToManyField(Movie)  # Change the related_name

    def __str__(self):
        return self.title

class Request(models.Model):
    url = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.url}"

class RequestCount(models.Model):
    date = models.DateField()
    count = models.IntegerField()

    def __str__(self):
        return f"{self.date} - {self.count}"
    