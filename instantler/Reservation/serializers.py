from rest_framework import serializers
from .models import *


class ReservationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationInfo
        fields = ('id','restaurant','user', 'type', 'guestNum')

class PastOrderReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastOrderReview
        fields = ('id','restaurant', 'user', 'rating', 'description')  # user is the User's id
