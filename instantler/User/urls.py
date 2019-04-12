from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'preferences', PreferenceViewSet)
router.register(r'user-type', UserTypeViewSet)
urlpatterns = router.urls
