from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'table-type', TableTypeViewSet, basename='tabletype')
router.register(r'table-data', TableDataViewSet, basename='tabledata')
urlpatterns = router.urls
