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

class UserVector(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    american = models.IntegerField(default=0)
    seafood = models.IntegerField(default=0)
    steak = models.IntegerField(default=0)
    fast = models.IntegerField(default=0)
    bar = models.IntegerField(default=0)
    finedining = models.IntegerField(default=0)
    chinese = models.IntegerField(default=0)
    japanese =  models.IntegerField(default=0)
    korean = models.IntegerField(default=0)
    mexican = models.IntegerField(default=0)
    pizza = models.IntegerField(default=0)
    breakfast = models.IntegerField(default=0)
    noodle = models.IntegerField(default=0)
    italian = models.IntegerField(default=0)
    mediterranean = models.IntegerField(default=0)
    french = models.IntegerField(default=0)
    vegetarian = models.IntegerField(default=0)
