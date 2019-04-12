from django.db import models
from Table.models import TableType
from Restaurant.models import Restaurant
from django.contrib.auth.models import User

class ReservationInfo(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(TableType, on_delete=models.CASCADE)
    guestNum = models.IntegerField(default=1)

class PastOrderReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(TableType, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    description = models.TextField()
