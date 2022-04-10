from django.contrib import admin
from .models import Business, BusinessField, ServiceType, Counties, BotUser, City


# Register your models here.

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']
    fields = (('name', 'owner',), ('county', 'city'),
              'about', 'email', 'phone', 'telegram', 'insta')
    readonly_fields = ('owner', 'name', 'county', 'city')


@admin.register(BusinessField)
class BusinessFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']


@admin.register(Counties)
class CountiesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']


@admin.register(BotUser)
class BotUser(admin.ModelAdmin):
    list_display = ['uid', 'username']
    list_display_links = ['uid']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'county']
