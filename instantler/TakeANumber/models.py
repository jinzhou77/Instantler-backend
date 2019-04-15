from django.db import models
from Table.models import TableType
from Restaurant.models import Restaurant
from django.contrib.auth.models import User

class WSNumber(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    waitingNumber = models.IntegerField(default=0)
    servedNumber = models.IntegerField(default=0)

class WaitingUser(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    myNumber = models.IntegerField()
    first_name = models.CharField(max_length=100, null = True)
