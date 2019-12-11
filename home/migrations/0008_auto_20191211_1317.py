# Generated by Django 2.1.7 on 2019-12-11 04:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20191211_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='expire',
            field=models.DateTimeField(choices=[(datetime.datetime(2019, 12, 14, 13, 17, 39, 640040), '3 Days'), (datetime.datetime(2019, 12, 18, 13, 17, 39, 640040), '7 days'), (datetime.datetime(2020, 1, 10, 13, 17, 39, 640040), '30 days')], default=datetime.datetime(2019, 12, 12, 13, 17, 39, 640040)),
        ),
        migrations.AlterField(
            model_name='product',
            name='explanation',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='statustype',
            field=models.CharField(choices=[('S', 'Sold'), ('E', 'Expired'), ('R', 'Running')], default='R', max_length=1),
        ),
    ]
