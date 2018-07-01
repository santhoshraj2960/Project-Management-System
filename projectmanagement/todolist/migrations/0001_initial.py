# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=140)),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('due_date', models.DateField(null=True, blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('completed_date', models.DateField(null=True, blank=True)),
                ('note', models.TextField(null=True, blank=True)),
                ('assigned_to', models.ForeignKey(related_name='todo_assigned_to', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('created_by', models.ForeignKey(related_name='todo_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
