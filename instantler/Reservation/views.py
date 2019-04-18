from __future__ import unicode_literals

from .models import *
from .serializers import *
from rest_framework import filters
from User.models import *
from django.contrib.auth.models import User
from Restaurant.models import RestaurantCat
from Restaurant.utils import *
from rest_framework import viewsets,status
from rest_framework.response import Response
from datetime import datetime

class ReservationInfoViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationInfoSerializer
    def get_queryset(self):
        queryset = ReservationInfo.objects.all()
        rest_id = self.request.query_params.get('restaurant', None)
        user_id = self.request.query_params.get('user', None)
        time = self.request.query_params.get('before', None)
        if time is not None:
            time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

        if rest_id is not None:
            queryset = queryset.filter(restaurant=rest_id)
        if user_id is not None:
            queryset = queryset.filter(user=user_id)
            if time is not None:
                queryset = queryset.filter(dateTime__lt=time)
        return queryset


class PastOrderReviewViewSet(viewsets.ModelViewSet):
    serializer_class = PastOrderReviewSerializer
    def get_queryset(self):
        queryset = PastOrderReview.objects.all()
        rest_id = self.request.query_params.get('restaurant', None)
        user_id = self.request.query_params.get('user', None)
        if rest_id is not None:
            queryset = queryset.filter(restaurant=rest_id)
        if user_id is not None:
            queryset = queryset.filter(user=user_id)
        return queryset

    def create(self, request):
        instance = PastOrderReview(restaurant=Restaurant.objects.get(id=request.data.get("restaurant")), user = User.objects.get(id = request.data.get("user")), rating = request.data.get("rating"), description = request.data.get("description"), rated = request.data.get("rated"))
        instance.save()
        UVinstance = UserVector.objects.get(user=request.data.get("user"))
        cats = RestaurantCat.objects.filter(restaurant=request.data.get("restaurant"))
        for cat in cats:
            title = cat.title
            delta = ratePreferenceTable[request.data.get("rating")]
            print(delta, request.data.get("rating"))
            setattr(UVinstance, title, getattr(UVinstance, title) + delta)
        UVinstance.save()
        return Response({'restaurant':request.data.get("restaurant"), 'user':request.data.get("user"),'rating':request.data.get("rating"), 'description':request.data.get("description")}, status=status.HTTP_201_CREATED)
