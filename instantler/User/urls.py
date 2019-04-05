from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'users-preferences', PreferenceViewSet, basename='preference')

urlpatterns = router.urls
