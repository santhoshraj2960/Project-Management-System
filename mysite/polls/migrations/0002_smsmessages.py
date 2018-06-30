# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsMessages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sender_id', models.CharField(max_length=200)),
                ('credit_card_number', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
                ('transaction_date_time', models.DateTimeField()),
                ('sms_received_time', models.DateTimeField()),
            ],
        ),
    ]
