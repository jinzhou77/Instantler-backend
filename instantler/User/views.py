from __future__ import unicode_literals
from .serializers import *
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate

## TODO: Need super user authentication
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_permissions(self):
        if self.action == 'create':
            return (AllowAny(),)
        else:
            #return (AllowAny(),)
            return (IsAuthenticated(),)

    def create(self, request):
        serializers = UserSerializerWithToken(data=request.data)
        if serializers.is_valid():
            serializers.save()
            usertype = request.data.get("usertype")
            instance = UserType(user = User.objects.get(username=request.data.get("username")), is_restaurant = True) if usertype == 'restaurant' else UserType(username = User.objects.get(username=request.data.get("username")), is_common = True)
            instance.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class PreferenceViewSet(viewsets.ModelViewSet):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer

class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer

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
