from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=140)
    description = models.CharField(max_length=1000, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='todo_created_by', on_delete=models.CASCADE)

# Table to track any changes in status of tasks
class TaskStatus(models.Model):
    user = models.ForeignKey(User, related_name='task_status_changed_by', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    status_change_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    task = models.ForeignKey(Task, related_name='task_status_changed_by', on_delete=models.CASCADE)