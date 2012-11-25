#!/usr/bin/env python
# -*- coding: utf-8 -*-

from intranet.utils.shortcuts import render_with_context
from intranet.urls import app
from streaming.models import Channel, Video
from intranet.settings.local_settings import TWITCH_API, STREAM_UPDATE

from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.utils.timezone import now

import urllib.request
import json

view = app.view(__name__, root=r'^streams/')

view.simple('^list_streams.js$', 'list_streams.js')

@view.route('^$')
def streams(request):
  return render_with_context(request, 'streams.html')


@view.route('^add/$')
def add_stream(request):
  status, messages, content = process_add(request)
  result = {
      'status' : status,
      'messages' : messages,
      'content' : content,
      }
  return HttpResponse(json.dumps(result), mimetype="application/json")


def json_request(url):
  fp = urllib.request.urlopen(url)
  content = fp.read()
  content = content.decode('utf-8')
  return json.loads(content)

def process_add(request):
  status = 'success'
  messages = list()
  result = list()
  if not 'channel' in request.GET:
    status = 'error'
    messages.append('No channel to add')
    return status, messages, result
  channels = set(request.GET['channel'].split(','))
  db_channels = Channel.objects.filter(name__in=channels).values('name')
  already = set(channel['name'] for channel in db_channels)
  wrong = channels.intersection(already)
  if wrong:
    status = 'warning'
    messages.append('Channel already exists : {channels}'.format(channels=', '.join(wrong)))
  todo = channels - already
  for channel in todo:
    item = Channel(name=channel)
    item.save()
    messages.append('{channel} added'.format(channel=channel))
    channel_info = update_channel(channel)
    result.append(channel_info.to_dict())
  return status, messages, result

def update_channel(channel, data=None):
  item = Channel.objects.get(name=channel)
  if not data:
    data = json_request(TWITCH_API['channel'].format(channel=channel))
  for field in ('name', 'display_name', 'logo', 'status', 'game', 'url'):
    setattr(item, field, data[field])
    item.channel_timestamp = now()
    item.save()
  return item


@view.route('^update/$')
def update_streams(request):
  channels = set(item['name']
      for item in Channel.objects.values('name'))
  data = json_request(TWITCH_API['stream'].format(channels=','.join(channels)))
  good = set()
  for stream in data['streams']:
    name = stream['channel']['name']
    good.add(name)
    item = update_channel(name, stream['channel'])
    if item.streaming == False:
      item.streaming = True
    item.stream_timestamp = now()
    item.save()
  todo = channels - good

  toupdate = Channel.objects.filter(name__in=todo, streaming=True).update(streaming=False)
  Channel.objects.filter(name__in=todo).update(stream_timestamp=now())
  result = [item.to_dict() for item  in Channel.objects.all()]

  return HttpResponse(json.dumps(result), mimetype='application/json')

@view.route('^channels/$')
def get_channels(request):
  result = [channel.to_dict() for channel in Channel.objects.order_by('name').all()]
  return HttpResponse(json.dumps(result), mimetype='application/json')

@view.route('^videos/$')
def get_videos(request):
  return HttpResponse()
