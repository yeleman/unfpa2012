#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.shortcuts import render

from bolibana.models import Entity
from bolibana.web.decorators import provider_required

from unfpa_core.models import ChildrenMortalityReport


def weekly_monthly_children(request, period, rtype):
    context = {'period': period, 'category': 'unfpa',
               'subcategory': 'children'}
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


def quarterly_annual_children(request, period, rtype):
    context = {'period': period, 'category': 'unfpa',
               'subcategory': 'children'}
    data = []
    months = period.months

    # total deaths for all districts
    # /!\ UNFPA districts only
    all_deaths = ChildrenMortalityReport.periods.within(period).count()

    # for each district
    for district in Entity.objects.filter(type__slug='district'):
        mdeaths = []
        for month in months:
            nb_deaths = ChildrenMortalityReport.periods.within(month) \
                           .filter(death_location__in=district
                                   .get_descendants()) \
                           .count()
            mdeaths.append(nb_deaths)
        total = sum(mdeaths)
        data.append({'district': district, 'mdeaths': mdeaths,
                     'total': total, 'all_deaths': all_deaths,
                     'percent_of_all': float(total) / all_deaths})

    context.update({'data': data, 'type': rtype, 'months': months})

    return render(request, 'quarterly_annual_children.html', context)


@provider_required
def quarterly_children(request, period):
    return quarterly_annual_children(request, period, 'quarterly')


@provider_required
def annual_children(request, period):
    return quarterly_annual_children(request, period, 'annual')
