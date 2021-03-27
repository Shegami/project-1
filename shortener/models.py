from django.db import models
from datetime import datetime


class Shortener(models.Model):
    full_url = models.URLField()
    short_url = models.URLField(unique=True)
    clicks = models.IntegerField(default=0)
    create_date = models.DateField(default=datetime.now)

    def __str__(self):
        return f'{self.short_url}'
