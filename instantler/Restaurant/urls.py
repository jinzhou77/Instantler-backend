from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'restaurants-cat', RestaurantCatViewSet, basename='restaurantCat')
router.register(r'restaurants-review', RestaurantReviewViewSet, basename='restaurantReview')

urlpatterns = router.urls