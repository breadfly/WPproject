# Generated by Django 2.1.7 on 2019-12-12 17:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20191213_0248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='expire',
            field=models.DateTimeField(choices=[(datetime.datetime(2019, 12, 15, 17, 50, 22, 337299, tzinfo=utc), '3 Days'), (datetime.datetime(2019, 12, 19, 17, 50, 22, 337299, tzinfo=utc), '7 days'), (datetime.datetime(2020, 1, 11, 17, 50, 22, 337299, tzinfo=utc), '30 days')], default=datetime.datetime(2019, 12, 15, 17, 50, 22, 337299, tzinfo=utc)),
        ),
    ]
