# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todolist', '0002_task_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.BooleanField(default=False)),
                ('status_change_date', models.DateField(auto_now_add=True, null=True)),
                ('task', models.ForeignKey(related_name='task_status_changed_by', to='todolist.Task')),
                ('user', models.ForeignKey(related_name='task_status_changed_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
