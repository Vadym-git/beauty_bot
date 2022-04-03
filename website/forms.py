from django.forms import ModelForm, EmailField
from beauty.models import Business, ServiceType
from django.db import models


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        # fields = '__all__'
        exclude = ('owner',)


class ServiceTypeForm(ModelForm):
    class Meta:
        model = ServiceType
        # fields = '__all__'
        exclude = ('owner',)