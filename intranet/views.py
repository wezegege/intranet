#!/usr/bin/env python
# -*- coding: utf-8 -*-

from intranet.urls import app

view = app.view(__name__)

view.simple(('^$','^home/$'), 'home.html')

view.simple('^git/$', 'git.html')
view.simple('^music/$', 'music.html')
view.simple('^config/$', 'config.html')
view.simple('^torrents/$', 'torrents.html')
view.simple('^home/$', 'home.html')
