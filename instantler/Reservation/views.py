from __future__ import unicode_literals

from .models import *
from .serializers import *
from rest_framework import filters
from User.models import *
from django.contrib.auth.models import User
from Restaurant.models import *
from Restaurant.utils import *
from rest_framework import viewsets,status
from rest_framework.response import Response
from datetime import datetime
from .utils import *
from Table.models import *

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

    def create(self, request):
        # assume we have spare table left
        restaurant = request.data.get("restaurant")
        user = request.data.get("user")
        first_name = request.data.get("first_name", "")
        type = request.data.get("type")
        dateTime = request.data.get("dateTime")
        guestNum = request.data.get("guestNum")
        instance = ReservationInfo(restaurant=Restaurant.objects.get(id=restaurant), user=User.objects.get(id=user), first_name=first_name,type=TableType.objects.get(id=type), dateTime=dateTime,guestNum=guestNum)
        instance.save()
        sql = "UPDATE \"Table_tabledata\" SET \"remainNum\" = \"remainNum\" -1 WHERE \"tableType_id\"={} AND \"dateTime\" = \'{}\';".format(type,dateTime)
        executeSQL(sql)
        #table_data_obj = TableData.objects.get(tableType=type,dateTime=dateTime)
        #table_data_obj.remainNum = table_data_obj.remainNum -1
        #table_data_obj.save()
        return Response({'id':instance.id,'restaurant':restaurant, 'user':user,'first_name':first_name, 'type':type,'dateTime':dateTime,'guestNum':guestNum}, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        if ReservationInfo.objects.filter(id=pk).exists():
            # add table first
            instance = ReservationInfo.objects.get(id=pk)
            print(instance.type,instance.dateTime)
            #sql = "UPDATE \"Table_tabledata\" SET \"remainNum\" = \"remainNum\" +1 WHERE \"tableType_id\"={} AND \"dateTime\" = \'{}\';".format(instance.type,instance.dateTime)
            #executeSQL(sql)
            table_data_obj = TableData.objects.get(tableType=instance.type,dateTime=instance.dateTime)
            table_data_obj.remainNum = table_data_obj.remainNum + 1
            table_data_obj.save()
            sql = "DELETE FROM \"Reservation_reservationinfo\" WHERE id = {};".format(pk)
            executeSQL(sql)
            return Response({'message':'Successful delete'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'The reservation does not exist'}, status=status.HTTP_400_BAD_REQUEST)


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
        # create default value
        rest_id = request.data.get("restaurant")
        user_id = request.data.get("user")
        rating = request.data.get("rating", 4)
        description = request.data.get("description", "")
        rated = request.data.get("rated", False)

        instance = PastOrderReview(restaurant=Restaurant.objects.get(id=request.data.get("restaurant")), user = User.objects.get(id = request.data.get("user")), rating = request.data.get("rating"), description = request.data.get("description"), rated = request.data.get("rated"))
        instance.save()

        #sql = "INSERT INTO \"Reservation_pastorderreview\"(restaurant_id, user_id, rating, description, rated) VALUES({},{},{},\'{}\',{})".format(rest_id,user_id,rating,description,rated)
        #executeSQL(sql)

        UVinstance = UserVector.objects.get(user=request.data.get("user"))

        cats = RestaurantCat.objects.raw("SELECT * FROM \"Restaurant_restaurantcat\" WHERE restaurant_id = {}".format(rest_id))

        #cats = RestaurantCat.objects.filter(restaurant=request.data.get("restaurant"))
        for cat in cats:
            title = cat.title
            delta = ratePreferenceTable[request.data.get("rating")]
            setattr(UVinstance, title, getattr(UVinstance, title) + delta)
        UVinstance.save()
        return Response({'id':instance.id, 'restaurant':request.data.get("restaurant"), 'user':request.data.get("user"),'rating':request.data.get("rating"), 'description':request.data.get("description"), 'rated':rated}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        rest_id = request.data.get("restaurant")
        user_id = request.data.get("user")
        rating = request.data.get("rating", 4)
        description = request.data.get("description", "")
        rated = request.data.get("rated", False)

        instance = PastOrderReview.objects.get(id=pk)
        instance.rating = rating
        instance.description = description
        instance.rated = rated
        instance.save()
        rest_obj = Restaurant.objects.get(id=rest_id)
    
        temp = rest_obj.ratings_count * rest_obj.rating + rating
        rest_obj.ratings_count = rest_obj.ratings_count + 1
        rest_obj.rating = temp / rest_obj.ratings_count

        rest_obj.save()
        return Response({'id':instance.id,'restaurant':rest_id, 'user':user_id,'rating':rating, 'description':description, 'rated':rated}, status=status.HTTP_200_OK)
