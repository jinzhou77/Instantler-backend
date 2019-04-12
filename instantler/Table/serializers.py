from rest_framework import serializers
from .models import TableType, TableData
from datetime import datetime, date



class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = ('id', 'restaurant', 'type', 'supportedNum')

class TableDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableData
        fields = ('id', 'tableType', 'restaurant', 'remainNum', 'dateTime')
