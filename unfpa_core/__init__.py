#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from unfpa_core.models import UEntity


def unfpa_districts():
    return UEntity.objects.filter(type__slug='district') \
                         .filter(is_unfpa=True)


def credos_districts():
    return UEntity.objects.filter(type__slug='district') \
                         .filter(is_credos=True)