from rest_framework import serializers
from .models import *

class WSNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = WSNumber
        fields = ('id', 'restaurant', 'waitingNumber', 'servedNumber')

class WaitingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaitingUser
        fields = ('id', 'user', 'restaurant', 'myNumber', 'first_name')
