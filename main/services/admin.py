from django.contrib import admin

from .models import (
    Service,
    Setting,
    Template,
)



class SettingAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Setting, SettingAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Template, None)
