# Generated by Django 3.1 on 2021-05-15 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0007_auto_20210515_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='totalb',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='totalp',
        ),
    ]