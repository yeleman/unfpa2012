#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou


from django.shortcuts import render
from bolibana.models import MonthPeriod
from unfpa_core.models import BirthReport


def sum_month(month):
    reports = BirthReport.objects.filter(created_on__gte=month.start_on,
                                             created_on__lte=month.end_on)
    indicator = {'month': month, 'birth': 0, 'residence': 0, 'center': 0,
                 'other': 0, 'male': 0, 'female': 0, 'alive': 0,
                 'stillborn': 0}

    for report in reports:
        indicator['birth'] += 1
        if report.birth_location == BirthReport.HOME:
            indicator['residence'] += 1
        if report.birth_location == BirthReport.CENTER:
            indicator['center'] += 1
        if report.birth_location == BirthReport.OTHER:
            indicator['other'] += 1
        if report.sex == BirthReport.MALE:
            indicator['male'] += 1
        if report.sex == BirthReport.FEMALE:
            indicator['female'] += 1
        if report.born_alive == True:
            indicator['alive'] += 1
        if report.born_alive == False:
            indicator['stillborn'] += 1

    return indicator


def birth(request):
    context = {'category': 'birth', 'eg': 'birth'}

    indicators = []
    for month in MonthPeriod.objects.all().order_by('start_on'):
        indicator = sum_month(month)
        indicators.append(indicator)

    context.update({'indicators': indicators})

    return render(request, 'birth.html', context)
