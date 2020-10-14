# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from network.models import Like, Post, Following

admin.site.register(Like)
admin.site.register(Post)
admin.site.register(Following)
