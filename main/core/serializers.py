from __future__ import (
    absolute_import,
)

from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rest_framework.serializers import (
    ListSerializer,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)


class BaseListSerializer(ListSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        
        super(BaseSerializer, self).__init__(*args, **kwargs)
        
        if fields:
            for field in set(self.fields.keys()) - set(fields):
                self.fields.pop(field)
        
        if exclude:
            for field in exclude:
                self.fields.pop(field, None)


class BaseModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        
        super(BaseModelSerializer, self).__init__(*args, **kwargs)
        
        if fields:
            for field in set(self.fields.keys()) - set(fields):
                self.fields.pop(field)
        
        if exclude:
            for field in exclude:
                self.fields.pop(field, None)


class BaseSerializer(Serializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        
        super(BaseSerializer, self).__init__(*args, **kwargs)
        
        if fields:
            for field in set(self.fields.keys()) - set(fields):
                self.fields.pop(field)
        
        if exclude:
            for field in exclude:
                self.fields.pop(field, None)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 10
    
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })
        
        
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'limit'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })
