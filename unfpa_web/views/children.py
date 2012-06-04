#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.shortcuts import render

from bolibana.models import Entity
from bolibana.web.decorators import provider_required

from unfpa_core.models import ChildrenMortalityReport


def weekly_monthly_children(request, period, rtype):
    context = {'period': period}
    data = []
    for district in Entity.objects.filter(type__slug='district'):
        nb_deaths = ChildrenMortalityReport.periods.within(period) \
                       .filter(death_location__in=district.get_descendants()) \
                       .count()
        data.append({'district': district, 'deaths': nb_deaths})

    context.update({'data': data, 'type': rtype})

    return render(request, 'weekly_monthly_children.html', context) 


@provider_required
def weekly_children(request, period):
    return weekly_monthly_children(request, period, 'weekly')
    

@provider_required
def monthly_children(request, period):
    return weekly_monthly_children(request, period, 'monthly')
