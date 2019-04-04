from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Preference


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined')


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ('user', 'preference')  # user is the User's id
