#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou

from django.shortcuts import render
from django.db.models import Q
from nosmsd.models import Inbox, SentItems

from bolibana.web.decorators import provider_permission
from bolibana.models import MonthPeriod
from unfpa_core import all_periods
from unfpa_core.models import (BirthReport, ChildrenMortalityReport,
                               PregnancyReport, UEntity)

from unfpa_web.views.data import current_period


@provider_permission('can_view_indicator_data')
def credos_dashboard(request):
    context = {'category': 'credos', 'subcategory': 'credos_dashboard'}

    periods = list(all_periods(MonthPeriod))[-15:]

    period = current_period()

    all_credos_center = UEntity.objects.filter(is_credos=True).all().count()

    # nb de decés infantile
    total_children_death = ChildrenMortalityReport.objects \
                            .filter(source=ChildrenMortalityReport.CREDOS) \
                            .count()
    last_children_death = ChildrenMortalityReport.periods \
                                                 .within(period) \
                         .filter(source=ChildrenMortalityReport.CREDOS) \
                         .count()

    # nb de naissance
    total_birth = BirthReport.objects \
                         .filter(source=BirthReport.CREDOS) \
                         .count()
    last_birth = BirthReport.periods.within(period) \
                         .filter(source=BirthReport.CREDOS) \
                         .count()

    # nb de grossesse
    total_pregnancy = PregnancyReport.objects \
                         .filter(source=PregnancyReport.CREDOS) \
                         .count()
    last_pregnancy = PregnancyReport.periods \
                                    .within(period) \
                                    .filter(source=PregnancyReport.CREDOS) \
                                    .count()

    # message
    all_inbox_qs = Inbox.objects.filter(
                              Q(textdecoded__startswith=u"fnuap born") |
                              Q(textdecoded__startswith=u"fnuap gpw") |
                              Q(textdecoded__startswith=u"fnuap du5 c"))
    all_inbox = all_inbox_qs.count()
    all_sent_qs = SentItems.objects.filter(
                              Q(textdecoded__startswith=u"fnuap born") |
                              Q(textdecoded__startswith=u"fnuap gpw") |
                              Q(textdecoded__startswith=u"fnuap du5 c"))
    all_sent = all_sent_qs.count()
    last_inbox = all_inbox_qs \
                         .filter(receivingdatetime__gte=period.start_on,
                                 receivingdatetime__lte=period.end_on) \
                         .count()
    last_sent = all_sent_qs \
                         .filter(deliverydatetime__gte=period.start_on,
                                 deliverydatetime__lte=period.end_on) \
                         .count()

    evol_data = {'children': {'label': u"Décès", 'values': {}},
                 'pregnancy': {'label': u"Grossesses", 'values': {}},
                 'birth': {'label': u"Naissances", 'values': {}}}
    for period in periods:
        nb_children = ChildrenMortalityReport.periods.within(period) \
                                    .filter(source=PregnancyReport.CREDOS) \
                                    .count()
        nb_pregnancy = PregnancyReport.periods.within(period) \
                                    .filter(source=PregnancyReport.CREDOS) \
                                    .count()
        nb_birth = BirthReport.periods.within(period) \
                                    .filter(source=PregnancyReport.CREDOS) \
                                    .count()
        evol_data['children']['values'][period.pid] = {'value': nb_children}
        evol_data['pregnancy']['values'][period.pid] = {'value': nb_pregnancy}
        evol_data['birth']['values'][period.pid] = {'value': nb_birth}

    context.update({'period': period,
                    'all_credos_center': all_credos_center,
                    'all_inbox': all_inbox,
                    'all_sent': all_sent,
                    'last_sent': last_sent,
                    'last_inbox': last_inbox,
                    'total_birth': total_birth,
                    'last_birth': last_birth,
                    'total_pregnancy': total_pregnancy,
                    'last_pregnancy': last_pregnancy,
                    'total_children_death': total_children_death,
                    'last_children_death': last_children_death,
                    'periods': periods,
                    'evol_data': evol_data.items()})

    return render(request, 'credos_dashboard.html', context)
