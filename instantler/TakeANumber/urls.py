from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'wsnumber', WSNumberViewSet, basename="wsnumber")
router.register(r'waiting-user', WaitingUserViewSet, basename="waitinguser")
urlpatterns = router.urls
