from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response

## TODO: Need super user authentication
class WSNumberViewSet(viewsets.ModelViewSet):

    serializer_class = WSNumberSerializer

    def get_queryset(self):
        queryset = WSNumber.objects.all()
        rest_id = self.request.query_params.get('restaurant', None)
        if rest_id is not None:
            queryset = queryset.filter(restaurant=rest_id)
        return queryset

class WaitingUserViewSet(viewsets.ModelViewSet):

    serializer_class = WaitingUserSerializer

    def get_queryset(self):
        queryset = WaitingUser.objects.all()
        rest_id = self.request.query_params.get('restaurant', None)
        user_id = self.request.query_params.get('user', None)
        if rest_id is not None:
            queryset = queryset.filter(restaurant=rest_id)
        if user_id is not None:
            queryset = queryset.filter(user=user_id)
        return queryset
