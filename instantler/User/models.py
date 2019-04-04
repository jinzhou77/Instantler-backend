from django.db import models
from django.contrib.auth.models import User


class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preference = models.CharField(max_length=30, null=True)
