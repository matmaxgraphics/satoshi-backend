# Generated by Django 3.2.9 on 2021-12-10 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionhistory',
            name='expiry_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='subscriptionhistory',
            name='start_date',
            field=models.DateField(),
        ),
    ]