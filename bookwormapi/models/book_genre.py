from django.db import models


class BookGenre(models.Model):
    label = models.CharField(max_length=50)