# Generated by Django 4.0.3 on 2022-04-02 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beauty', '0003_service_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='phone',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='telegram',
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
    ]