import datetime

from django.db import models


class Reader(models.Model):
    code = models.CharField(max_length=128)
    full_name = models.CharField(max_length=128)
    reg_date = models.DateField(default=datetime.date.today)
