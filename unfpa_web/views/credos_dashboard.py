#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou

from django.shortcuts import render
from nosmsd.models import Inbox, SentItems

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

    # nb de decés infantile
    total_children = ChildrenMortalityReport.objects.all().count()
    last_total_children = ChildrenMortalityReport.periods \
                                                 .within(period).count()

    # nb de naissance
    total_birth = BirthReport.objects.all().count()
    last_total_birth = BirthReport.periods.within(period).count()

    # nb de grossesse
    total_pregnancy = PregnancyReport.objects.all().count()
    last_total_pregnancy = PregnancyReport.periods \
                                          .within(period).count()

    # message
    received = Inbox.objects.count()
    sent = SentItems.objects.count()
    last_received = Inbox.objects \
                         .filter(receivingdatetime__gte=period.start_on,
                                 receivingdatetime__lte=period.end_on) \
                         .count()
    last_sent = SentItems.objects \
                         .filter(deliverydatetime__gte=period.start_on,
                                 deliverydatetime__lte=period.end_on) \
                         .count()

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

    context.update({'period': period,
                    'total_birth': total_birth,
                    'last_total_birth': last_total_birth,
                    'total_children': total_children,
                    'last_total_children': last_total_children,
                    'total_pregnancy': total_pregnancy,
                    'last_total_pregnancy': last_total_pregnancy,
                    'received': received,
                    'sent':sent, 'last_sent': last_sent,
                    'last_received': last_received,
                    'periods': periods,
                    'evol_data': evol_data.items()})

    return render(request, 'credos_dashboard.html', context)
