from rest_framework import serializers

from .models import (
    Service,
    Setting,
    Template
)
from core.serializers import BaseModelSerializer
        
        
class SettingSerializer(BaseModelSerializer):
    identifier = serializers.SerializerMethodField()
    
    class Meta:
        model = Setting
        exclude = ('created_at', 'updated_at',)
        
    def get_identifier(self,obj):
        return obj.get_identifier_display()


class ServiceSerializer(BaseModelSerializer):
    settings = SettingSerializer(many=True)
    identifier = serializers.SerializerMethodField()
    service_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        exclude = ('created_at', 'updated_at',)
        
    def get_identifier(self,obj):
        return obj.get_identifier_display()
        
    def get_service_type(self,obj):
        return obj.get_service_type_display()
        
        
class TemplateSerializer(BaseModelSerializer):
    
    class Meta:
        model = Template
        exclude = ('created_at', 'updated_at',)
