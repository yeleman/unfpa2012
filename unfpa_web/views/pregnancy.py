#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad


from django.shortcuts import render

from bolibana.models import MonthPeriod
from bolibana.web.decorators import provider_permission
from unfpa_core import all_periods
from unfpa_core.models import PregnancyReport
from unfpa_web.views.data import rate_cal


def sum_month(month):
    reports = PregnancyReport.periods.within(month) \
                         .filter(source=PregnancyReport.CREDOS)
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


@provider_permission('can_view_indicator_data')
def pregnancy(request):
    context = {'category': 'credos', 'subcategory': 'pregnancy'}

    periods = all_periods(MonthPeriod)

    indicators = []

    evol_data = {'fe': {'label': u"Total femmes enceintes", 'values': {}},
                 'ae': {'label': u"Accouchement enregistrés", 'values': {}},
                 'gi': {'label': u"Grossesses interrompues", 'values': {}},
                 'av': {'label': u"Grossesses avec enfants vivants",
                        'values': {}},
                 'mn': {'label': u"Grossesses avec morts nées", 'values': {}}}

    for month in periods:
        indicator = sum_month(month)
        indicators.append(indicator)
        indicator['rate_fe'] = rate_cal(indicator['fe'], indicator['fe'])
        indicator['rate_ae'] = rate_cal(indicator['ae'], indicator['fe'])
        indicator['rate_gi'] = rate_cal(indicator['gi'], indicator['fe'])
        indicator['rate_av'] = rate_cal(indicator['av'], indicator['fe'])
        indicator['rate_mn'] = rate_cal(indicator['mn'], indicator['fe'])
        evol_data['fe']['values'][month.pid] = {'value': indicator['fe']}
        evol_data['ae']['values'][month.pid] = {'value': indicator['ae']}
        evol_data['gi']['values'][month.pid] = {'value': indicator['gi']}
        evol_data['av']['values'][month.pid] = {'value': indicator['av']}
        evol_data['mn']['values'][month.pid] = {'value': indicator['mn']}

    context.update({'indicators': indicators,
                    'evol_data': evol_data.items(),
                    'periods': periods})

    return render(request, 'pregnancy.html', context)
