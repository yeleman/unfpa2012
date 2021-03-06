#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad

from django.shortcuts import render
from django.db.models import Q
from nosmsd.models import Inbox, SentItems

from bolibana.web.decorators import provider_permission
from bolibana.models import MonthPeriod
from unfpa_core.models import (RHCommoditiesReport, MaternalMortalityReport,
                               ChildrenMortalityReport, UEntity)
from unfpa_web.views.data import current_period
from unfpa_core import all_periods


@provider_permission('can_view_indicator_data')
def unfpa_dashboard(request):
    context = {'category': 'unfpa', 'subcategory': 'unfpa_dashboard'}

    periods = list(all_periods(MonthPeriod))[-15:]

    period = current_period()

    all_unfpa_center = UEntity.objects.filter(is_unfpa=True).all().count()

    all_inbox_qs = Inbox.objects.filter(
                              Q(textdecoded__startswith=u"fnuap dpw") |
                              Q(textdecoded__startswith=u"fnuap mps") |
                              Q(textdecoded__startswith=u"fnuap du5 f"))
    all_inbox = all_inbox_qs.count()
    all_sent_qs = SentItems.objects.filter(
                              Q(textdecoded__startswith=u"fnuap dpw") |
                              Q(textdecoded__startswith=u"fnuap mps") |
                              Q(textdecoded__startswith=u"fnuap du5 f"))
    all_sent = all_sent_qs.count()
    last_inbox = all_inbox_qs \
                         .filter(receivingdatetime__gte=period.start_on,
                                 receivingdatetime__lte=period.end_on) \
                         .count()
    last_sent = all_sent_qs \
                         .filter(deliverydatetime__gte=period.start_on,
                                 deliverydatetime__lte=period.end_on) \
                         .count()

    total_children_death = ChildrenMortalityReport.objects \
                                .filter(source=ChildrenMortalityReport.UNFPA) \
                                .count()
    last_children_death = ChildrenMortalityReport.periods \
                            .within(period) \
                            .filter(source=ChildrenMortalityReport.UNFPA) \
                            .count()
    total_maternal_death = MaternalMortalityReport.objects \
                            .filter(source=MaternalMortalityReport.UNFPA) \
                            .count()
    last_maternal_death = MaternalMortalityReport.periods.within(period) \
                            .filter(source=MaternalMortalityReport.UNFPA) \
                            .count()

    total_3methods_out = sum([1
                        for report
                        in RHCommoditiesReport.validated.all()
                        if report.fp_stockout_3methods()])

    last_3methods_out = sum([1
                        for report
                        in RHCommoditiesReport.validated.filter(period=period)
                        if report.fp_stockout_3methods()])

    context.update({'period': period,
                    'all_unfpa_center': all_unfpa_center,
                    'all_inbox': all_inbox,
                    'all_sent': all_sent,
                    'last_inbox': last_inbox,
                    'last_sent': last_sent,
                    'total_children_death': total_children_death,
                    'last_children_death': last_children_death,
                    'total_maternal_death': total_maternal_death,
                    'last_maternal_death': last_maternal_death,
                    'total_3methods_out': total_3methods_out,
                    'last_3methods_out': last_3methods_out})

    evol_data = {'children': {'label': u"Mortalité infantile", 'values': {}},
                 'maternal': {'label': u"Mortalité maternelle", 'values': {}}}

    for period in periods:
        nb_children = ChildrenMortalityReport.periods.within(period) \
                            .filter(source=ChildrenMortalityReport.UNFPA) \
                            .count()
        nb_maternal = MaternalMortalityReport.periods.within(period) \
                            .filter(source=MaternalMortalityReport.UNFPA) \
                            .count()
        evol_data['children']['values'][period.pid] = {'value': nb_children}
        evol_data['maternal']['values'][period.pid] = {'value': nb_maternal}

    context.update({'periods': periods,
                    'evol_data': evol_data.items()})

    return render(request, 'unfpa_dashboard.html', context)
