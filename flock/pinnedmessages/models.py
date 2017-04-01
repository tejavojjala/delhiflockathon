from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

import bleach

# Create your models here.

class MessagesManager(models.Manager):
	def create_message(self,flock_user, flock_user_name, userDp, groupId, isPinned, text, messageUid):
		message = self.create(userId = flock_user, userName = flock_user_name, userDp = userDp, groupId = groupId, isPinned = isPinned, text = text, messageUid = messageUid)
		return message

class Messages(models.Model):
	primaryKey = models.AutoField(primary_key=True)
	userId = models.CharField(max_length = 100)
	date =  models.DateTimeField(auto_now_add=True)
	userName = models.CharField(max_length = 100)
	userDp = models.CharField(max_length = 1000)
	groupId = models.CharField(max_length = 100)
	isPinned = models.BooleanField(default=False)
	text = models.CharField(max_length=2000)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	messageUid = models.CharField(max_length=100)
	objects = MessagesManager()

class ReactionsManager(models.Manager):
	def create_reaction(self,foreignKey, reactorId, reactionType):
		reaction = self.create(foreignKey = foreignKey, reactorId = reactorId, reactionType = reactionType)
		return reaction

class Reactions(models.Model):
	foreignKey = models.ForeignKey(Messages, on_delete = models.CASCADE)
	reactorId = models.CharField(max_length = 100)
	reactionType = models.CharField(max_length = 20)
	objects = ReactionsManager()

class UsersManager(models.Manager):
	def create_user(self, userToken, userId):
		user = self.create(userToken = userToken, userId = userId)
		return user

class Users(models.Model):
	userToken = models.CharField(max_length = 100)
	userId = models.CharField(max_length = 100)
	objects = UsersManager()

#class Comments(models.Model):

