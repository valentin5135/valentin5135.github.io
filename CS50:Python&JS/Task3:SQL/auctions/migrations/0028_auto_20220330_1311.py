# Generated by Django 2.2.12 on 2022-03-30 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0027_auto_20220330_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='follow',
            field=models.BooleanField(default=False),
        ),
    ]