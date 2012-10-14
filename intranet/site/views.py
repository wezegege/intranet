#!/usr/bin/env python
# -*- coding: utf-8 -*-

from intranet.utils.shortcuts import render_with_context
from intranet.site import app
import urllib
import json

view = app.view(__name__)

view.simple(('^$','^home/$'), 'home.html')

@view.route('^streams/$')
def streams(request):
  streams = list()
  types = {
      'twitch' : 'Twitch.tv',
      'daily' : 'Dailymotion',
      }
  ups = {
      False : 'info',
      True : 'success',
      }
  users = [
      ('mistermv', 'twitch'),
      ('Mynthos', 'twitch'),
      ('Siglemic', 'twitch'),
      ('Breakdown777', 'twitch'),
      ('Werster', 'twitch'),
      ('EssentiaFour', 'twitch'),
      ('lethalfrag', 'twitch'),
      ('barrylesjambes', 'twitch'),
      ('Mikwuyma', 'twitch'),
      ]
  streams = [dict(
    (('user', user), ('type', {'id' : type_id, 'name' : types[type_id]})))
    for user, type_id in users]
  #for user, type_id in users:
  #  data = {
  #      'user' : user,
  #      'type' : {
  #        'id' : type_id,
  #        'name' : types[type_id],
  #        },
  #      }
  #  r = urllib.request.urlopen('http://api.justin.tv/api/stream/list.json?channel={user}'.format(user=user))
  #  response = r.read().decode('utf-8')
  #  result = json.loads(response)
  #  if result:
  #    result = result[0]
  #    data['up'] = {
  #        'value' : True,
  #        'class' : ups[True],
  #        }
  #    data['game'] = result['meta_game']
  #    data['since'] = result['up_time']
  #    data['title'] =  result['title']
  #    data['embed'] = result['channel']['embed_code']
  #    data['channel'] = result['channel']['channel_url']
  #    data['image'] = result['channel']['image_url_small']
  #  else:
  #    data['up'] = {
  #        'value' : False,
  #        'class' : ups[False],
  #        }
  #    data['game'], data['since'] = '', ''
  #    r = urllib.request.urlopen('http://api.justin.tv/api/channel/show/{user}.json'.format(user=user))
  #    response = r.read().decode('utf-8')
  #    result = json.loads(response)
  #    if result:
  #      data['title'] = result['status']
  #      data['embed'] = result['embed_code']
  #      data['channel'] = result['channel_url']
  #      data['image'] = result['image_url_small']
  #  r = urllib.request.urlopen('http://api.justin.tv/api/channel/archives/{user}.json?limit=3'.format(user=user))
  #  response = r.read().decode('utf-8')
  #  result = json.loads(response)
  #  if result:
  #    data['videos'] = list()
  #    for item in result:
  #      video = {
  #          'date' : item['start_time'],
  #          'length' : item['length'],
  #          'title' : item['title'],
  #          }
  #  streams.append(data)

  return render_with_context(request, 'streams.html',
      {'streams': streams})

view.simple('^git/$', 'git.html')
view.simple('^music/$', 'music.html')
view.simple('^config/$', 'config.html')
view.simple('^torrents/$', 'torrents.html')
view.simple('^home/$', 'home.html')
