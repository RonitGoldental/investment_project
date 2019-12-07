# Generated by Django 2.2.7 on 2019-12-06 19:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_auto_20191204_1036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalrate',
            old_name='dividend_paid',
            new_name='dividend_amount',
        ),
        migrations.AddField(
            model_name='currentrate',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 6, 19, 21, 28, 94465, tzinfo=utc)),
        ),
    ]