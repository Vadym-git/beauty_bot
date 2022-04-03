from django.contrib import admin
from .models import Business, BusinessField, ServiceType


# Register your models here.

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessField)
class BusinessFieldAdmin(admin.ModelAdmin):
    pass

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']

# @admin.register(City)
# class CityAdmin(admin.ModelAdmin):
#     pass


# @admin.register(District)
# class DistrictAdmin(admin.ModelAdmin):
#     pass
