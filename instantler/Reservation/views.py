from __future__ import unicode_literals

from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework import filters

class ReservationInfoViewSet(viewsets.ModelViewSet):
    queryset = ReservationInfo.objects.all()
    serializer_class = ReservationInfoSerializer

class PastOrderReviewViewSet(viewsets.ModelViewSet):
    queryset = PastOrderReview.objects.all()
    serializer_class = PastOrderReviewSerializer
