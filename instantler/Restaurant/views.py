from __future__ import unicode_literals

from .models import *
from .serializers import *
from rest_framework import viewsets


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantCatViewSet(viewsets.ModelViewSet):
    queryset = RestaurantCat.objects.all()
    serializer_class = RestaurantCatSerializer

class RestaurantReviewViewSet(viewsets.ModelViewSet):
    queryset = RestaurantReview.objects.all()
    serializer_class = RestaurantReviewSerializer

