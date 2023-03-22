from django.db import models


class Book(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    released_date = models.DateField()
    length = models.IntegerField()
    description = models.CharField(max_length=150)
    book_genre = models.ForeignKey(
        "BookGenre", on_delete=models.CASCADE, related_name="BookGenre_book")
    reader = models.ForeignKey(
        "Reader", on_delete=models.CASCADE, related_name="reader_book")
    image_url = models.CharField(max_length=200)

    @property
    def creator(self):
        return self.__creator

    @creator.setter
    def creator(self, value):
        self.__creator = value