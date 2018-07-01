from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=140)
    description = models.CharField(max_length=1000, null=True)
    created_date = models.DateField(auto_now_add=True, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True, )
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='todo_created_by', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        User, blank=True, null=True, related_name='todo_assigned_to', on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True)