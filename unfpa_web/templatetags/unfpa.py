#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django import template

register = template.Library()

@register.filter(name='yesnostock')
def yesnostock(value):
    return u"Yes" if value == 0 else u"No"