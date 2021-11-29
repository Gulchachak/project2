# Generated by Django 3.2.8 on 2021-11-26 03:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_bid_bid_new_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='buyer',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]