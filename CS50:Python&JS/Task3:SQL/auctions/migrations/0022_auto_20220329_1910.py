# Generated by Django 2.2.12 on 2022-03-29 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_auto_20220329_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bet',
            name='min_bet',
        ),
        migrations.AlterField(
            model_name='bet',
            name='current_bet',
            field=models.IntegerField(),
        ),
    ]
