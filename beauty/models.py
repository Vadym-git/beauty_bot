from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class City(models.Model):
#     name = models.CharField(verbose_name='City', max_length=32)
#
#     class Meta:
#         db_table = 'cities'
#
#     def __str__(self):
#         return self.name


# class District(models.Model):
#     name = models.CharField(verbose_name='District', max_length=32)
#     city = models.ForeignKey(City, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'districts'
#
#     def __str__(self):
#         return self.name


class BusinessField(models.Model):
    """Type of business, like: beauty, photo, healthcare"""
    name = models.CharField(verbose_name='Business field', max_length=64)
    description = models.TextField()

    class Meta:
        db_table = 'business_field'

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    name = models.CharField(verbose_name='Service', max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=1.0)
    description = models.TextField()
    owner = models.ForeignKey('Business', on_delete=models.CASCADE)


class Business(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Business name', max_length=64, default='Business name')
    city = models.CharField(verbose_name='City', max_length=64, default='city')
    type_of_business = models.ForeignKey(BusinessField, on_delete=models.SET_NULL, null=True)
    about = models.TextField(verbose_name='About business', default='')
    email = models.EmailField(default='', blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=16)
    telegram = models.CharField(blank=True, null=True, max_length=24)

    def __str__(self):
        return self.name
