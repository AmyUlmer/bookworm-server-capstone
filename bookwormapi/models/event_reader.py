from django.db import models


class EventReader(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    reader = models.ForeignKey("Reader", on_delete=models.CASCADE)
