# Generated by Django 3.2.9 on 2021-12-19 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0009_auto_20211219_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionhistory',
            name='email',
            field=models.EmailField(max_length=200),
        ),
    ]
