from django.db import models

from Django.readers.models import Reader


class Book(models.Model):
    code = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    year = models.IntegerField()
    language = models.CharField(max_length=64)
    is_available = models.BooleanField()
    reader = models.ForeignKey(Reader, null=True)
