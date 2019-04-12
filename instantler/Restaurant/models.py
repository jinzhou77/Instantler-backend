# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .utils import uuidToStr
from User.models import *

'''
class Rest(models.Model):
    rest = models.CharField(primary_key=True, default=uuidToStr, max_length=100)

    def __str__(self):
        return self.rest

class RestLoc(models.Model):
    rest = models.ForeignKey(Rest, on_delete=models.CASCADE, default=uuidToStr)
    address = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=10)

    def __str__(self):
        return self.address if self.address else "null"

class RestCat(models.Model):
    rest = models.ForeignKey(Rest, on_delete=models.CASCADE, default=uuidToStr)
    title = models.CharField(max_length=50)

class RestInfo(models.Model):
    rest = models.ForeignKey(Rest, on_delete=models.CASCADE, default=uuidToStr)
    name = models.CharField(max_length=100)
    photo_url = models.CharField(max_length=200)

    def __str__(self):
        return self.name
'''

class Restaurant(models.Model):
    yelp_id = models.CharField(default=uuidToStr, max_length=100,blank=True)
    address = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    photo_url = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    ratings_sum = models.BigIntegerField(default=0)
    ratings_count = models.IntegerField(default=0)


class RestaurantCat(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

'''
class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    ratings = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
'''
