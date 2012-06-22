#!/usr/bin/env python
# encoding=utf-8
# maintainer:

from django.shortcuts import render

from bolibana.models import MonthPeriod
from bolibana.web.decorators import provider_permission
from unfpa_core.models import ChildrenMortalityReport
from unfpa_web.views.data import rate_cal
from unfpa_core import all_periods


def sum_month(month):
    child_reports = ChildrenMortalityReport.periods.within(month) \
                         .filter(source=ChildrenMortalityReport.CREDOS)

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


@provider_permission('can_view_indicator_data')
def death(request):
    context = {'category': 'credos', 'subcategory': 'death'}

    indicators = []
    periods = all_periods(MonthPeriod)

    evol_data = {'ntd': {'label': u"Total décès", 'values': {}},
                 'dd': {'label': u"Domicile", 'values': {}},
                 'dc': {'label': u"Centre", 'values': {}},
                 'da': {'label': u"Ailleurs", 'values': {}},
                 'sm': {'label': u"Sexe masculin", 'values': {}},
                 'sf': {'label': u"Sexe feminin", 'values': {}}}

    for month in periods:
        indicator = sum_month(month)
        indicators.append(indicator)
        indicator['rate_ntd'] = rate_cal(indicator['ntd'], indicator['ntd'])
        indicator['rate_dd'] = rate_cal(indicator['dd'], indicator['ntd'])
        indicator['rate_dc'] = rate_cal(indicator['dc'], indicator['ntd'])
        indicator['rate_da'] = rate_cal(indicator['da'], indicator['ntd'])
        indicator['rate_sm'] = rate_cal(indicator['sm'], indicator['ntd'])
        indicator['rate_sf'] = rate_cal(indicator['sf'], indicator['ntd'])

        evol_data['ntd']['values'][month.pid] = {'value': indicator['ntd']}
        evol_data['dd']['values'][month.pid] = {'value': indicator['dd']}
        evol_data['dc']['values'][month.pid] = {'value': indicator['dc']}
        evol_data['da']['values'][month.pid] = {'value': indicator['da']}
        evol_data['sm']['values'][month.pid] = {'value': indicator['sm']}
        evol_data['sf']['values'][month.pid] = {'value': indicator['sf']}

    context.update({'indicators': indicators,
                    'evol_data': evol_data.items(),
                    'periods': periods})

    return render(request, 'death.html', context)
