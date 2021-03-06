# Generated by Django 2.2.12 on 2022-03-28 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20220327_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='description',
            field=models.TextField(default='SOME DESCRIPTION'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='photo',
            field=models.ImageField(blank=True, default='photos/no_photo.png', max_length=1024, upload_to='photos'),
        ),
    ]
