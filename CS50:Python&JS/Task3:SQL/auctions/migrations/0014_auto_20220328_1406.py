# Generated by Django 2.2.12 on 2022-03-28 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20220328_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='price',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='auction',
            name='status',
            field=models.CharField(default='active', max_length=16),
        ),
    ]
