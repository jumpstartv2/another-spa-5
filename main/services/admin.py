from django.contrib import admin

from .models import (
    Service,
    Setting,
)


class SettingInline(admin.TabularInline):
    model = Service.settings.through
    extra = 0


class SettingAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = (SettingInline,)


admin.site.register(Setting, SettingAdmin)
admin.site.register(Service, ServiceAdmin)
