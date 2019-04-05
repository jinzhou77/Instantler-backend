from __future__ import unicode_literals
from .serializers import *
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return (AllowAny(),)
        else:
            return (IsAuthenticated(),)

    def create(self, request):
        serializers = UserSerializerWithToken(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class PreferenceViewSet(viewsets.ModelViewSet):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer