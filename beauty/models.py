from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.

class BotUser(models.Model):
    first_name = models.CharField(verbose_name='First name', max_length=48, null=True, blank=True)
    uid = models.PositiveBigIntegerField()
    language = models.CharField(max_length=8, null=True, blank=True)
    username = models.CharField(max_length=64, null=True, blank=True)
    date_reg = models.DateTimeField(verbose_name='Registration date', blank=True, null=True)
    connect_date = models.DateTimeField(verbose_name='Last connection date', blank=True, null=True)
    county = models.ForeignKey('Counties', on_delete=models.SET_NULL, null=True, blank=True)
    # city = models.CharField(verbose_name='City', max_length=64)

    @staticmethod
    def check_registration(user: dict):
        user_id = user['id']
        first_name = user.get('first_name')
        username = user.get('username')
        language = user.get('language_code')
        try:
            user = BotUser.objects.get(uid=user_id)
            user.first_name = first_name
            user.uid = user_id
            user.username = username
            user.language = language
            user.connect_date = now()
            user.save()
        except BotUser.DoesNotExist:
            BotUser(uid=user_id, first_name=first_name, language=language, username=username, date_reg=now(),
                    connect_date=now()).save()
        return user_id


class Counties(models.Model):
    name = models.CharField(verbose_name='County', max_length=32, unique=True)

    class Meta:
        db_table = 'counties'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(verbose_name='City', max_length=32)
    county = models.ForeignKey(Counties, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'cities'

    def __str__(self):
        return self.name


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
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey('Business', on_delete=models.CASCADE)


class Business(models.Model):
    owner = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(verbose_name='Business name', max_length=64, default='Business name')
    county = models.ForeignKey(Counties, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    type_of_business = models.ForeignKey(BusinessField, on_delete=models.SET_NULL, null=True, blank=True)
    about = models.TextField(verbose_name='About business', default='', blank=True, null=True)
    email = models.EmailField(default='', blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=16, default='+353')
    telegram = models.CharField(blank=True, null=True, max_length=24, default='account_name')
    insta = models.CharField(blank=True, null=True, max_length=24, default='account_name')

    def __str__(self):
        return self.name
