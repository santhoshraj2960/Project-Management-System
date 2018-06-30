from django.db import models

# Create your models here.

from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class SmsMessages(models.Model):
	sender_id = models.CharField(max_length=200)
	credit_card_number = models.CharField(max_length=50)
	amount = models.FloatField()
	transaction_date_time = models.DateTimeField()
	sms_received_time = models.DateTimeField()