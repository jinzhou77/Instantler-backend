from django.db import models
from Table.models import TableType
from Restaurant.models import Restaurant
from django.contrib.auth.models import User
from datetime import datetime, date
from django.db.models import DateTimeField

class ReservationInfo(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    type = models.ForeignKey(TableType, on_delete=models.CASCADE)
    dateTime = DateTimeField(auto_now=False, null=True)
    guestNum = models.IntegerField(default=1)


class PastOrderReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)
    description = models.TextField(null=True)
    rated = models.BooleanField(default=False)
