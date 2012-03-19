#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from unfpa_web import urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include(urls)),
    url(r'^admin/', include(admin.site.urls)),
)
