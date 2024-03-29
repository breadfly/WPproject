# Generated by Django 2.1.7 on 2019-12-11 03:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20191211_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buyer', to='home.User'),
        ),
        migrations.AlterField(
            model_name='product',
            name='expire',
            field=models.DateTimeField(choices=[(datetime.datetime(2019, 12, 14, 12, 57, 31, 563309), '3 Days'), (datetime.datetime(2019, 12, 18, 12, 57, 31, 563309), '7 days'), (datetime.datetime(2020, 1, 10, 12, 57, 31, 563309), '30 days')], default=datetime.datetime(2019, 12, 12, 12, 57, 31, 563309)),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
