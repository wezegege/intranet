#!/usr/bin/env python
# -*- coding: utf-8 -*-

from  django.db import models

class Channel(models.Model):
  name = models.CharField(max_length=30)
  game = models.CharField(max_length=30, blank=True, null=True)
  display_name = models.CharField(max_length=30)
  streaming = models.BooleanField(default=False)
  url = models.URLField(blank=True, null=True)
  status = models.CharField(max_length=30, blank=True, null=True)
  logo = models.URLField(blank=True, null=True)
  channel_timestamp = models.DateTimeField(null=True, blank=True)
  stream_timestamp = models.DateTimeField(null=True, blank=True)
  video_timestamp = models.DateTimeField(null=True, blank=True)
  followers = models.ManyToManyField('auth.user')

  def to_dict(self):
    return dict((
      (field, getattr(self, field))
      for field in ('name', 'display_name', 'streaming',
        'url', 'status', 'logo', 'game')
      ))

class Video(models.Model):
  channel = models.ForeignKey(Channel)
  name = models.CharField(max_length=30)
  url = models.URLField()
  date = models.DateTimeField()

