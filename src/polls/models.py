from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

import datetime


@python_2_unicode_compatible  #for python 2 support
class Question(models.Model):
	""" Model for storing information about the Question """
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('Date Published')
	category = models.CharField(max_length=50,null=True)
	

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days = 1) <= self.pub_date <= now
		
		was_published_recently.admin_order_field = 'pub_date'
		was_published_recently.boolean = True
		was_published_recently.short_description = 'Published recently?'




@python_2_unicode_compatible  #for python 2 support
class Choice(models.Model):
	"""Choice for the Questions present in the Database"""
	question = models.ForeignKey(Question, 
								on_delete=models.CASCADE)
	
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	

	def __str__(self):
		return self.choice_text