#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad


from django.shortcuts import render
from bolibana.models import MonthPeriod
from unfpa_core.models import PregnancyReport


def sum_month(month):
    reports = PregnancyReport.objects.filter(created_on__gte=month.start_on,
                                             created_on__lte=month.end_on)
    indicator = {'month': month, 'fe': 0, 'ae': 0, 'gi': 0, 'av': 0, 'mn': 0}

    for report in reports:
        indicator['fe'] += 1
        if report.delivery_date:
            indicator['ae'] += 1
        if report.pregnancy_result == PregnancyReport.ABORTION:
            indicator['gi'] += 1
        if report.pregnancy_result == PregnancyReport.ALIVE:
            indicator['av'] += 1
        if report.pregnancy_result == PregnancyReport.STILLBORN:
            indicator['mn'] += 1

    return indicator


def pregnancy(request):
    context = {'category': 'pregnancy', 'eg': 'pregnancy'}

    indicators = []
    for month in MonthPeriod.objects.all().order_by('start_on'):
        indicator = sum_month(month)
        indicators.append(indicator)

    context.update({'indicators': indicators})

    return render(request, 'pregnancy.html', context)
