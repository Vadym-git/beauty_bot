# Generated by Django 4.0.3 on 2022-04-01 17:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Business field')),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'business_field',
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Service')),
                ('description', models.TextField()),
                ('business_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beauty.businessfield')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Business name', max_length=64, verbose_name='Business name')),
                ('city', models.CharField(default='city', max_length=64, verbose_name='City')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('type_of_business', models.ManyToManyField(to='beauty.businessfield')),
            ],
        ),
    ]
