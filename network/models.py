# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.CharField(max_length=20)
    content = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now=True, blank=True)

class Like(models.Model):
    post_id = models.IntegerField()
    user = models.CharField(max_length=20)

class Following(models.Model):
    user = models.CharField(max_length=20)
    following =models.CharField(max_length=20)