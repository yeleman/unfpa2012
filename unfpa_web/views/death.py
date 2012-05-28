#!/usr/bin/env python
# encoding=utf-8
# maintainer:

from django.shortcuts import render
from bolibana.models import MonthPeriod
from unfpa_core.models import ChildrenMortalityReport


def sum_month(month):
    child_reports = ChildrenMortalityReport.objects\
                                     .filter(created_on__gte=month.start_on,
                                             created_on__lte=month.end_on)

    indicator = {'month': month, 'ntd': 0, 'dd': 0, 'dc': 0, 'da': 0, 'sm': 0,
                 'sf': 0}

    for report in child_reports:
        indicator['ntd'] += 1
        if report.death_place == ChildrenMortalityReport.HOME:
            indicator['dd'] += 1
        if report.death_place == ChildrenMortalityReport.CENTER:
            indicator['dc'] += 1
        if report.death_place == ChildrenMortalityReport.OTHER:
            indicator['da'] += 1
        if report.sex == ChildrenMortalityReport.MALE:
            indicator['sm'] += 1
        if report.sex == ChildrenMortalityReport.FEMALE:
            indicator['sf'] += 1

    return indicator


def death(request):

    context = {'category': 'death', 'eg': 'death'}

    indicators = []
    for month in MonthPeriod.objects.all().order_by('start_on'):
        indicator = sum_month(month)
        indicators.append(indicator)

    context.update({'indicators': indicators})

    return render(request, 'death.html', context)
