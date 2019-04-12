from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reservation', ReservationInfoViewSet, basename='reservation')
router.register(r'review', PastOrderReviewViewSet, basename='review')


urlpatterns = router.urls
