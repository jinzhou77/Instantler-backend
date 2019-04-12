from django.db import models
from django.contrib.auth.models import User

class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preference = models.CharField(max_length=30, null=True)

class UserType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_superUser = models.BooleanField(default=False)
    is_restaurant = models.BooleanField(default=False)
    is_common = models.BooleanField(default=False)
