# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0013_auto_20150620_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinvites',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 20, 23, 33, 14, 831616)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='updated_date_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 20, 23, 33, 14, 830977)),
        ),
    ]