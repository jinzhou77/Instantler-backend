from __future__ import unicode_literals
from .serializers import *
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from .models import *
from Restaurant.models import Restaurant
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from .permissions import UserPermission
from Restaurant.utils import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_permissions(self):
        if self.action == 'create' or self.action == 'retrieve':
            return (AllowAny(),)
        else:
            #return (AllowAny(),)
            return (IsAuthenticated(),UserPermission())


    def retrieve(self, request, pk=None):
        try:
            is_restaurant = UserType.objects.get(user=pk).is_restaurant
            user_obj = User.objects.get(id=pk)
            res = {}
            res["user"] = user_obj.id
            res["username"] = user_obj.username
            res["email"] = user_obj.email
            res["first_name"] = user_obj.first_name
            res["last_name"] = user_obj.last_name
            res["last_login"] = user_obj.last_login
            res["date_joined"] = user_obj.date_joined
            if is_restaurant:
                try:
                    restaurant = Restaurant.objects.get(user=pk).id
                except ObjectDoesNotExist:
                    restaurant = 0
                res["restaurant"] = restaurant
                return Response(res, status=status.HTTP_200_OK)
            else:
                return Response(res, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)



    def create(self, request):
        serializers = UserSerializerWithToken(data=request.data)
        if serializers.is_valid():
            serializers.save()
            try:
                usertype = request.data.get("usertype")
                instance = UserType(user = User.objects.get(username=request.data.get("username")), is_restaurant = True) if usertype == 'restaurant' else UserType(user = User.objects.get(username=request.data.get("username")), is_common = True)
                instance.save()
                if usertype == "common":
                    preference_list = request.data.get("preference", None)
                    if preference_list:
                        PreferenceViewSet.setPreference(User.objects.get(username=request.data.get("username")), preference_list)
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            except:
                instance = User.objects.get(username = request.data.get("username")).delete()
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class PreferenceViewSet(viewsets.ModelViewSet):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer

    def get_permissions(self):
        if self.action == 'create' and self.action == 'retrieve':
            return (AllowAny(),)
        else:
            #return (AllowAny(),)
            return (IsAuthenticated(),UserPermission())

    def retrieve(self, request, pk=None):
        ps = Preference.objects.filter(user = pk)
        l = []
        for p in ps:
            l += [p.preference]
        return Response({"user":pk, "perference":l}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if pk != request.user.id:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        self.setPreference(User.objects.get(id=pk), request.data.get("preference"))
        return Response({"user":pk, "preference":request.data.get("preference")}, status=status.HTTP_200_OK)


    @classmethod
    def setPreference(self, user_obj, p_list):
        if not UserType.objects.get(user = user_obj).is_common:
            return
        ps = Preference.objects.filter(user = user_obj.id)
        if ps:
            for p in ps:
                instance = UserVector.get(user=user_obj.id)
                setattr(instance, p, getattr(instance, p) - initPreferenceWeight)
                instance.save()
        for p in p_list:
            instance = Preference(user=user_obj, preference=p)
            instance.save()
            try:
                instance = UserVector.objects.get(user=user_obj.id)
            except ObjectDoesNotExist:
                instance = UserVector(user=user_obj)
            setattr(instance, p, getattr(instance, p) + initPreferenceWeight)
            instance.save()


class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
    def get_permissions(self):
        if self.action == 'create' and self.action == 'retrieve':
            return (AllowAny(),)
        else:
            return (IsAuthenticated(),UserPermission())

class UserVectorViewSet(viewsets.ModelViewSet):
    queryset = UserVector.objects.all()
    serializer_class = UserVectorSerializer


@csrf_exempt
@api_view(['POST',])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    is_restaurant = request.data.get("is_restaurant", False)
    if not is_restaurant:
        is_common = request.data.get("is_common", False)

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        if user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            userType = UserType.objects.get(user=user.id)
            if (userType.is_restaurant and is_restaurant) or (userType.is_common and is_common):
                return Response({'token': token.key, 'id': user.id}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Incorrect user type.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)
