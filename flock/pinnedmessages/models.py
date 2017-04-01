from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

import bleach

# Create your models here.

class MessagesManager(models.Manager):
	def create_message(self,flock_user, flock_user_name, groupId, isPinned, text):
		message = self.create(userId=flock_user, userName = flock_user_name, groupId = groupId, isPinned = isPinned, text = text)
		return message

class Messages(models.Model):
	primaryKey = models.AutoField(primary_key=True)
	userId = models.CharField(max_length = 100)
	userName = models.CharField(max_length = 100)
	groupId = models.CharField(max_length = 100)
	isPinned = models.BooleanField(default=False)
	text = models.CharField(max_length=2000)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	objects = MessagesManager()