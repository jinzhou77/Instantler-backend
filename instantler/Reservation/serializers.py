from rest_framework import serializers
from .models import *


class ReservationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationInfo
        fields = ('id','type','restaurant', 'user', 'guestNum')

class PastOrderReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastOrderReview
        fields = ('id','user','table', 'rating', 'description')  # user is the User's id
