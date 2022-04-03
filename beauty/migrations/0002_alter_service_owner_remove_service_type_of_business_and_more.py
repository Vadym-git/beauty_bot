# Generated by Django 4.0.3 on 2022-04-01 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('beauty', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='service',
            name='type_of_business',
        ),
        migrations.AddField(
            model_name='service',
            name='type_of_business',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='beauty.businessfield'),
        ),
    ]
