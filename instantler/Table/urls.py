from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'table-type', TableTypeViewSet)
router.register(r'table-data', TableDataViewSet)
urlpatterns = router.urls
