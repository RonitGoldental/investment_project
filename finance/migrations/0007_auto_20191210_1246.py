# Generated by Django 2.2.7 on 2019-12-10 12:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_auto_20191207_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentrate',
            name='time_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 10, 12, 46, 6, 583128, tzinfo=utc)),
        ),
    ]
