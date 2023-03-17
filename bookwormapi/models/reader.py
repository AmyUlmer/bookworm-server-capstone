from django.db import models
from django.contrib.auth.models import User


class Reader(models.Model):
    # Relationship to the built-in User model- has name and email
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional bio field to capture from the client
    bio = models.CharField(max_length=150)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
