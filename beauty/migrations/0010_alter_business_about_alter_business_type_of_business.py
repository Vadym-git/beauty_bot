# Generated by Django 4.0.3 on 2022-04-04 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beauty', '0009_business_insta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='about',
            field=models.TextField(blank=True, default='', null=True, verbose_name='About business'),
        ),
        migrations.AlterField(
            model_name='business',
            name='type_of_business',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='beauty.businessfield'),
        ),
    ]