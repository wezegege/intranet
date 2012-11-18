#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

SITE_NAME='Intranet'

TWITCH_API = {
    'stream' : 'https://api.twitch.tv/kraken/streams?channel={channels}',
    'channel' : 'https://api.twitch.tv/kraken/channels/{channel}',
    }

STREAM_UPDATE = {
    'video' : timedelta(hours=-12),
    'channel' : timedelta(hours=-3),
    'stream' : timedelta(seconds=-30),
    }
