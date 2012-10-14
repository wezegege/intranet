#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf.urls import patterns, url
import os.path

class Application(object):
    def __init__(self):
        self.views = list()

    def view(self, name):
        result = View(name)
        self.views.append(result)
        return result

    def patterns(self):
        result = patterns('')
        for view in self.views:
            result += view.pattern()
        return result

class View(object):
    def __init__(self, module):
        self.module = module
        self.urls = list()
        self.simples = list()

    def route(self, pattern, *args, **kwargs):
        def func_wrapper(func):
            self.urls.append(url(pattern, func.__name__,
                        name=func.__name__, *args, **kwargs))
            return func
        return func_wrapper

    def simple(self, patterns, template, *args, **kwargs):
        if isinstance(patterns, str):
            patterns = (patterns,)
        for pattern in patterns:
            self.simples.append(url(pattern, 'render_with_context',
                {'template': template}, *args,
                name=os.path.basename(template).split('.')[0],
                **kwargs))

    def pattern(self):
        result = patterns(self.module, *self.urls)
        if self.simples:
            result += patterns('intranet.utils.shortcuts',
                    *self.simples)
        return result

def render_with_context(request, template, *args, **kwargs):
    return render_to_response(template, *args,
        context_instance=RequestContext(request), **kwargs)
