# Generated by Django 2.2.12 on 2022-03-29 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_auto_20220329_1910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bet',
            name='bet_source',
        ),
        migrations.AlterField(
            model_name='auction',
            name='price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='last_bet', to='auctions.Bet'),
        ),
    ]