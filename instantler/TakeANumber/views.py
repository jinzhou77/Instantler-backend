from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from Restaurant.models import Restaurant
from django.contrib.auth.models import User

## TODO: Need super user authentication
class WSNumberViewSet(viewsets.ModelViewSet):

    serializer_class = WSNumberSerializer

    def get_queryset(self):
        queryset = WSNumber.objects.all()
        rest_id = self.request.query_params.get('restaurant', None)
        if rest_id is not None:
            queryset = queryset.filter(restaurant=rest_id)
        return queryset

    def update(self, request, pk=None):
        old_ins = WSNumber.objects.get(restaurant=pk)
        waitingNumber = request.data.get('waitingNumber', None)
        servedNumber = request.data.get('servedNumber', None)
        if waitingNumber is not None:
            old_ins.waitingNumber = waitingNumber
        if servedNumber is not None:
            old_ins.servedNumber = servedNumber
        old_ins.save()
        return Response({'restaurant':pk, 'waitingNumber':old_ins.waitingNumber, 'servedNumber':old_ins.servedNumber}, status=status.HTTP_200_OK)


class WaitingUserViewSet(viewsets.ModelViewSet):

    serializer_class = WaitingUserSerializer

    def get_queryset(self):
        queryset = WaitingUser.objects.all()
        rest_id = self.request.query_params.get('restaurant', None)
        myNumber = self.request.query_params.get('myNumber', None)

        if rest_id is not None:
            servedNumber = WSNumber.objects.get(restaurant=rest_id).servedNumber
            queryset = queryset.filter(restaurant=rest_id, myNumber__gte=servedNumber)
        if myNumber is not None:
            queryset = queryset.filter(myNumber=myNumber)
        return queryset

    def create(self, request):
        user = request.data.get("user")
        restaurant = request.data.get("restaurant")
        first_name = request.data.get("first_name")
        ws_obj = WSNumber.objects.get(restaurant=restaurant)
        ws_obj.waitingNumber = ws_obj.waitingNumber + 1
        ws_obj.save()
        myNumber = ws_obj.waitingNumber
        instance = WaitingUser(first_name=first_name,restaurant = Restaurant.objects.get(id=restaurant), user = User.objects.get(id=user), myNumber=myNumber)
        instance.save()
        return Response({'id':instance.id, 'restaurant':restaurant, 'user':user, 'first_name':first_name, 'myNumber':myNumber}, status=status.HTTP_201_CREATED)
