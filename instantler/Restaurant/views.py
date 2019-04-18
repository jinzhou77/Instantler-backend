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
from django.contrib.auth.models import User
from User.serializers import *
from TakeANumber.models import WSNumber

id= 400

class RestaurantViewSet(viewsets.ModelViewSet):

    serializer_class = RestaurantSerializer
    def get_queryset(self):
        user_id = self.request.query_params.get('user', None)
        isCommon = self.request.query_params.get('is_common', False)
        city = self.request.query_params.get('city', None)
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
                    if city and rest.restaurant.city == city:
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
                        if city and rest.city == city:
                            ids.add(rest.id)

                rest_lists = list(ids)
                random.shuffle(rest_lists)
                rest_lists = rest_lists[0:10]

                queryset = Restaurant.objects.filter(id__in=rest_lists)
            return queryset

        query = self.request.query_params.get('query', None)
        price = self.request.query_params.get('price', None)
        popular = self.request.query_params.get('popular', False)


        if popular:
            queryset = Restaurant.objects.order_by('-rating','-ratings_count')
        else:
            queryset = Restaurant.objects.all()

        if query is not None:
            #queryset = queryset.filter(name=name)
            rest_lists = Restaurant.objects.raw("(SELECT * FROM \"Restaurant_restaurant\" WHERE name LIKE \'%%{}%%\') UNION (SELECT * FROM \"Restaurant_restaurant\" WHERE address LIKE \'%%{}%%\');".format(query,query))
            queryset = Restaurant.objects.filter(id__in=map(lambda rest:rest.id, rest_lists))
        if city is not None:
            queryset = queryset.filter(city=city)
        if price is not None:
            queryset = queryset.filter(price=price)
        return queryset

    def update(self, request, pk):
        old_ins = Restaurant.objects.get(pk=pk)
        user = request.data.get('user')
        old_ins.address = request.data.get('address')
        old_ins.city = request.data.get('city')
        old_ins.state = request.data.get('state')
        old_ins.name = request.data.get('name')
        old_ins.photo_url = request.data.get('photo_url')
        old_ins.ratings_count = request.data.get('ratings_count')
        old_ins.rating = request.data.get('rating')
        old_ins.price = request.data.get('price')
        old_ins.phone_num = request.data.get('phone_num')
        l = request.data.get('categories', None)
        RestaurantCat.objects.filter(restaurant=old_ins.id).delete()
        old_ins.save()
        if l is not None:
            iniGen(old_ins, l)
        return Response({'id': old_ins.id, 'user': user, 'address': old_ins.address,'city': old_ins.city,'state': old_ins.state,'photo_url': old_ins.photo_url,'name': old_ins.name,'phone_num': old_ins.phone_num,'price': old_ins.price,'ratings_count': old_ins.ratings_count, 'rating':old_ins.rating,'categories':l}, status=status.HTTP_200_OK)

    def create(self, request):
        #global id
        #id = id + 1
        user = request.data.get('user')
        address = request.data.get('address')
        city = request.data.get('city')
        state = request.data.get('state')
        name = request.data.get('name')
        photo_url = request.data.get('photo_url')
        ratings_count = request.data.get('ratings_count',0)
        rating = request.data.get('rating',1.0)
        price = request.data.get('price','$$')
        phone_num = request.data.get('phone_num',0)
        l = request.data.get('categories', None)
        old_ins = Restaurant(user=User.objects.get(pk=user), address=address,city=city,state=state,name=name,photo_url=photo_url,ratings_count=ratings_count,rating=rating,price=price,phone_num=phone_num)
        old_ins.save()

        ws_ins = WSNumber(restaurant=old_ins)
        ws_ins.save()
        if l is not None:
            iniGen(old_ins, l)
        return Response({'id': old_ins.id, 'user': user, 'address': old_ins.address,'city': old_ins.city,'state': old_ins.state,'photo_url': old_ins.photo_url,'name': old_ins.name,'phone_num': old_ins.phone_num,'price': old_ins.price,'ratings_count': old_ins.ratings_count, 'rating':old_ins.rating,'catogories':l}, status=status.HTTP_201_CREATED)

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

def iniGen(restaurant, l):
    for cat in l:
        instance = RestaurantCat(restaurant = restaurant, title=cat)
        instance.save()
