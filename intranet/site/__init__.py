#!/usr/bin/env python
# -*- coding: utf-8 -*-

from intranet.utils.shortcuts import Application

app = Application()

import intranet.site.views

urlpatterns = app.patterns()
