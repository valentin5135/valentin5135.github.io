# Generated by Django 2.2.12 on 2022-03-27 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_remove_auction_pub_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='pub_data',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
