#!/usr/bin/env python
# -*- coding: utf-8 -*-

from intranet.settings import local_settings
from django.core.urlresolvers import reverse

def all(request):
  result = dict()
  for func in (constants, menu):
    result.update(func(request))
  return result


def constants(request):
  return {'constants' : local_settings}

def menu(request):
  items = [
      ('Home', 'home'),
      ('Streams', 'streams'),
      ('Music', 'music'),
      ('Torrents', 'torrents'),
      ('Git', 'git'),
      ('Config', 'config'),]
  return {'menu' : items}
