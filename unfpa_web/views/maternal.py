#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.shortcuts import render

from bolibana.models import Entity
from bolibana.web.decorators import provider_required

from unfpa_core.models import MaternalMortalityReport


def weekly_monthly_maternal(request, period, rtype):
    context = {'period': period}
    data = []
    for district in Entity.objects.filter(type__slug='district'):
        nb_deaths = MaternalMortalityReport.periods.within(period) \
                       .filter(pregnancy_related_death=True) \
                       .filter(death_location__in=district.get_descendants()) \
                       .count()
        data.append({'district': district, 'deaths': nb_deaths})

    context.update({'data': data, 'type': rtype})

    return render(request, 'weekly_monthly_maternal.html', context) 


@provider_required
def weekly_maternal(request, period):
    return weekly_monthly_maternal(request, period, 'weekly')


@provider_required
def monthly_maternal(request, period):
    return weekly_monthly_maternal(request, period, 'monthly')


def quarterly_annual_maternal(request, period, rtype):
    context = {'period': period}
    data = []
    months = period.months

    # total deaths for all districts
    # /!\ UNFPA districts only
    all_deaths = MaternalMortalityReport.periods.within(period) \
                           .filter(pregnancy_related_death=True) \
                           .count()

    # for each district
    for district in Entity.objects.filter(type__slug='district'):
        mdeaths = []
        for month in months:
            nb_deaths = MaternalMortalityReport.periods.within(month) \
                           .filter(pregnancy_related_death=True) \
                           .filter(death_location__in=district.get_descendants()) \
                           .count()
            mdeaths.append(nb_deaths)
        total = sum(mdeaths)
        data.append({'district': district, 'mdeaths': mdeaths,
                     'total': total, 'all_deaths': all_deaths,
                     'percent_of_all': float(total) / all_deaths})

    context.update({'data': data, 'type': rtype, 'months': months})

    return render(request, 'quarterly_annual_maternal.html', context) 


@provider_required
def quarterly_maternal(request, period):
    return quarterly_annual_maternal(request, period, 'quarterly')


@provider_required
def annual_maternal(request, period):
    return quarterly_annual_maternal(request, period, 'annual')