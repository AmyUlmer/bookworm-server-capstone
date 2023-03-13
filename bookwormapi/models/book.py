from django.db import models


class Book(models.Model):
    author = models.CharField(on_delete=models.CASCADE,  max_length=50)
    title = models.CharField(on_delete=models.CASCADE,  max_length=50)
    released_date = models.DateField()
    length = models.IntegerField()
    description = models.CharField(max_length=150)
    book_genre = models.ForeignKey("Genre", on_delete=models.CASCADE)