# Generated by Django 2.2.12 on 2022-03-27 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20220327_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='photo',
            field=models.BinaryField(default='auctions/source/no_photo.png', max_length=1024),
        ),
    ]
