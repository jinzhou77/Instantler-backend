from __future__ import unicode_literals

from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from User.models import UserVector
from .recommander import *
from Reservation.models import PastOrderReview
from .utils import columnNames
import random


class RestaurantViewSet(viewsets.ModelViewSet):

    serializer_class = RestaurantSerializer
    def get_queryset(self):
        user_id = self.request.query_params.get('user', None)
        isCommon = self.request.query_params.get('is_common', False)
        if user_id is not None:
            if not isCommon:
                queryset = Restaurant.objects.all()
                queryset = queryset.filter(user=user_id)
            else:
                ids = set()
                SUs = getSimilarUsers(user_id, 1)
                rest_lists = []
                rest_lists += PastOrderReview.objects.filter(user__in=SUs, rating__gt=3).order_by("-rating").only('restaurant')
                rest_lists += PastOrderReview.objects.filter(user=user_id, rating__gt=3).order_by("-rating").only('restaurant')
                i = 0
                for rest in rest_lists:
                    if i >= 4:
                        break
                    ids.add(rest.restaurant.id)
                    i += 1
                distr = getCategoryList(user_id, 10-i)
                rest_lists = []
                for index, count in enumerate(distr):
                    type = columnNames[index+1]
                    if not count:
                        continue
                    rest_lists += Restaurant.objects.raw("Select * from \"Restaurant_restaurant\" as T1 INNER JOIN \"Restaurant_restaurantcat\" as T2 ON T1.id = T2.restaurant_id WHERE title = \'{}\' Order By ratings_count*rating limit \'{}\';".format(type, count))
                    for rest in rest_lists:
                        ids.add(rest.id)

                rest_lists = list(ids)
                random.shuffle(rest_lists)
                rest_lists = rest_lists[0:10]

                queryset = Restaurant.objects.filter(id__in=rest_lists)
            return queryset

        name = self.request.query_params.get('name', None)
        address = self.request.query_params.get('address', None)
        city = self.request.query_params.get('city', None)
        price = self.request.query_params.get('price', None)
        popular = self.request.query_params.get('popular', False)
        if popular:
            queryset = Restaurant.objects.order_by('-rating','-ratings_count')
        else:
            queryset = Restaurant.objects.all()

        if name is not None:
            queryset = queryset.filter(name=name)
        if address is not None:
            queryset = queryset.filter(address=address)
        if city is not None:
            queryset = queryset.filter(city=city)
        if price is not None:
            queryset = queryset.filter(price=price)
        return queryset


class RestaurantCatViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantCatSerializer
    queryset = RestaurantCat.objects.all()

    def retrieve(self, request, pk=None):
        cat_l = RestaurantCat.objects.filter(restaurant=pk)
        l = []
        for c in cat_l:
            l += [c.title]
        return Response({"restaurant":pk, "categories":l}, status=status.HTTP_200_OK)

    def get_queryset(self):
        cat = self.request.query_params.get('catogory', None)
        queryset = RestaurantCat.objects.all()
        if cat is not None:
            queryset = queryset.filter(title=cat)
        return queryset
