from django.db import models

from Django.readers.models import Reader


class Book(models.Model):
    code = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    year = models.IntegerField()
    language = models.CharField(max_length=64)
    is_available = models.BooleanField(default=True)
    reader = models.ForeignKey(Reader, default=None, null=True)

