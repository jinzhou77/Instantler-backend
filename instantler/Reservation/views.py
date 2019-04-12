from __future__ import unicode_literals

from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework import filters

class ReservationInfoViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationInfoSerializer
    def get_queryset(self):
        queryset = ReservationInfo.objects.all()
        rest_id = self.request.query_params.get('restaurant', None)
        user_id = self.request.query_params.get('user', None)
        if rest_id is not None:
            queryset = queryset.filter(restaurant=rest_id)
        if user_id is not None:
            queryset = queryset.filter(user=user_id)
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
