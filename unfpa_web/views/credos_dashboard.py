#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad

from django.shortcuts import render

from bolibana.web.decorators import provider_required
from bolibana.models import MonthPeriod
from unfpa_core import all_periods
from unfpa_core.models import (BirthReport, ChildrenMortalityReport,
                               PregnancyReport)

from unfpa_web.views.data import current_period


@provider_required
def credos_dashboard(request):
    context = {'category': 'credos','subcategory': 'credos_dashboard'}

    period = current_period()
    total_children = ChildrenMortalityReport.objects.all().count()
    last_total_children = ChildrenMortalityReport.periods \
                                                 .within(period).count()
    total_pregnancy = PregnancyReport.objects.all().count()
    last_total_pregnancy = PregnancyReport.periods \
                                          .within(period).count()

    context.update({'period': period, 
                    'total_children': total_children,
                    'last_total_children': last_total_children,
                    'total_pregnancy': total_pregnancy,
                    'last_total_pregnancy': last_total_pregnancy})

    periods = all_periods(MonthPeriod)

    evol_data = {'children': {'label': u"Décès", 'values': {}},
                 'pregnancy': {'label': u"Grossesses", 'values': {}},
                 'birth': {'label': u"Naissances", 'values': {}}}
    for period in periods:
        nb_children = ChildrenMortalityReport.periods.within(period).count()
        nb_pregnancy = PregnancyReport.periods.within(period).count()
        nb_birth = BirthReport.periods.within(period).count()
        evol_data['children']['values'][period.pid] = {'value': nb_children}
        evol_data['pregnancy']['values'][period.pid] = {'value': nb_pregnancy}
        evol_data['birth']['values'][period.pid] = {'value': nb_birth}

    print(evol_data.values())
    for line in evol_data.values():
        print(line)
    context.update({'periods': periods,
                    'evol_data': evol_data.items()})

    return render(request, 'credos_dashboard.html', context)
