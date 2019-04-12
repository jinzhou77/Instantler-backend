from django.db import models
from Restaurant.models import Restaurant
from datetime import datetime, date
from django.db.models import DateTimeField


class TableType(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    type = models.CharField(max_length=30, null=True)
    supportedNum = models.IntegerField(default=1) # how many tables do we have

class TableData(models.Model):
    tableType = models.ForeignKey(TableType, on_delete=models.CASCADE)
    remainNum = models.IntegerField(default=0)
    dateTime = DateTimeField(auto_now=False)
