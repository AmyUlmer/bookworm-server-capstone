from django.db import models
from django.core.validators import MaxValueValidator


class Event(models.Model):
    event_name = models.CharField(on_delete=models.CASCADE,  max_length=50)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    host = models.ForeignKey("Host", on_delete=models.CASCADE)
    location = models.CharField(max_length=150)
    date_of_event = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    # MaxValueValidator(10) sets the maximum allowed value for max_capacity to 10.
    # try to create an instance of the Event model with a value of max_capacity greater than 10, you will get a validation error.
    max_capacity = models.PositiveIntegerField(
        validators=[MaxValueValidator(10)])

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
