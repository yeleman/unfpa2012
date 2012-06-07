#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from bolibana.models import Entity

UNFPA_DISTRICTS = ['mar', 'nio']
CREDOS_DISTRICTS = ['mar', 'nio']


def unfpa_districts():
    return Entity.objects.filter(type__slug='district') \
                         .filter(slug__in=UNFPA_DISTRICTS)


def credos_districts():
    return Entity.objects.filter(type__slug='district') \
                         .filter(slug__in=CREDOS_DISTRICTS)