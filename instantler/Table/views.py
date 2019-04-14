from .serializers import *
from rest_framework import viewsets, status
from .models import *
from Restaurant.models import Restaurant
from datetime import datetime,timedelta, date
from rest_framework.response import Response
from django.db import connection
import pytz

class TableTypeViewSet(viewsets.ModelViewSet):

    serializer_class = TableTypeSerializer

    def get_queryset(self):
        queryset = TableType.objects.all()
        rest_id = self.request.query_params.get('restaurant', None)
        if rest_id is not None:
            queryset = queryset.filter(restaurant=rest_id)
        return queryset

    def create(self, request):
        restaurant = request.data.get('restaurant')
        type = request.data.get('type')
        supportedNum = request.data.get('supportedNum')
        l = request.data.get('periods')
        totalNum = request.data.get('totalNum')
        instance = TableType(restaurant=Restaurant.objects.get(pk=restaurant), type=type, supportedNum=supportedNum)
        instance.save()
        iniGen(instance, l, totalNum)
        return Response({'restaurant': restaurant, 'type': type, 'supportedNum':supportedNum, 'totalNum':totalNum, 'periods':l}, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        old_ins = TableType.objects.get(pk=pk)
        type = request.data.get('type')
        restaurant = request.data.get('restaurant')
        supportedNum = request.data.get('supportedNum')
        l = request.data.get('periods')
        totalNum = request.data.get('totalNum')
        old_ins.type = type
        old_ins.supportedNum = supportedNum
        TableData.objects.filter(tableType=old_ins.id).delete()
        iniGen(old_ins, l, totalNum)
        return Response({'id':old_ins.id,'restaurant': restaurant, 'type': type, 'supportedNum':supportedNum, 'totalNum':totalNum, 'periods':l}, status=status.HTTP_200_OK)


class TableDataViewSet(viewsets.ModelViewSet):
    serializer_class = TableDataSerializer
    def get_queryset(self):
        queryset = TableData.objects.all()
        rest_id = self.request.query_params.get('restaurant', None)
        if rest_id is not None:
            queryset = queryset.filter(restaurant=rest_id)
        return queryset

def iniGen(TableType, l, total):
    for time in l:
        timeslot = datetime.strptime(time, "%H:%M:%S")
        today = datetime.today()
        st = datetime(today.year, today.month, today.day, timeslot.hour, timeslot.minute, timeslot.second, tzinfo=pytz.UTC)
        et = datetime(today.year, today.month+1, today.day, timeslot.hour, timeslot.minute, timeslot.second, tzinfo=pytz.UTC)
        timeslot = datetime.strptime(time, "%H:%M:%S")
        daySeq = [s for s in datetime_range(st, et, timedelta(days=1))]
        for d in daySeq:
            instance = TableData(tableType = TableType, restaurant= TableType.restaurant, remainNum=total, dateTime=d)
            instance.save()

def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta
