from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reservation', ReservationInfoViewSet)
router.register(r'review', PastOrderReviewViewSet)
#router.register(r'reviews', RestaurantReviewViewSet, basename='restaurantReview')

urlpatterns = router.urls
