# Generated by Django 4.0.3 on 2022-04-10 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beauty', '0009_remove_business_email_remove_business_insta_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='about',
        ),
    ]
