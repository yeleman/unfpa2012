#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad


from django.shortcuts import render
from bolibana.models import MonthPeriod
from unfpa_core.models import PregnancyReport
from unfpa_web.views.data import rate_cal
from datetime import datetime


def sum_month(month):
    reports = PregnancyReport.periods.within(month)
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
    context = {'category': 'credos', 'subcategory': 'pregnancy'}

    indicators = []
    for month in MonthPeriod.objects.filter(start_on__lt=datetime.now) \
                                    .order_by('start_on'):
        indicator = sum_month(month)
        indicators.append(indicator)
        indicator['rate_fe'] = rate_cal(indicator['fe'], indicator['fe'])
        indicator['rate_ae'] = rate_cal(indicator['ae'], indicator['fe'])
        indicator['rate_gi'] = rate_cal(indicator['gi'], indicator['fe'])
        indicator['rate_av'] = rate_cal(indicator['av'], indicator['fe'])
        indicator['rate_mn'] = rate_cal(indicator['mn'], indicator['fe'])

    context.update({'indicators': indicators})

    return render(request, 'pregnancy.html', context)
