# Generated by Django 2.2.12 on 2022-03-28 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auto_20220328_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='photo',
            field=models.ImageField(default='photos/no_photo.png', max_length=1024, upload_to='photos'),
        ),
    ]