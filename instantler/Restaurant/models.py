# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .utils import uuidToStr
from User.models import *
from django.contrib.auth.models import User


class Restaurant(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    yelp_id = models.CharField(default=uuidToStr, max_length=100,blank=True)
    address = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    photo_url = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    ratings_count = models.IntegerField(default=0)
    rating = models.IntegerField(default=1)
    phone_num = models.CharField(max_length=100, null=True)

class RestaurantCat(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
