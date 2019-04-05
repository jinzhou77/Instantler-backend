from rest_framework import serializers
from .models import *


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id','yelp_id', 'address', 'city', 'state', 'photo_url', 'zipcode','name')


class RestaurantCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantCat
        fields = ('id','restaurant', 'title')  # user is the User's id


class RestaurantReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id','restaurant', 'user', 'description', 'ratings', 'date')
