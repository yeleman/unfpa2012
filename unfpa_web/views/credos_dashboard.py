#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad

from django.shortcuts import render

from bolibana.web.decorators import provider_required
from unfpa_core.models import ChildrenMortalityReport, PregnancyReport

from unfpa_web.views.data import current_period


@provider_required
def credos_dashboard(request):
    context = {'category': 'credos','subcategory': 'credos_dashboard'}

    period = current_period()
    total_children = ChildrenMortalityReport.objects.all().count()
    last_total_children = ChildrenMortalityReport.objects \
                                .filter(created_on__gte=period.start_on,
                                        created_on__lte=period.end_on) \
                                .count()    
    total_pregnancy = PregnancyReport.objects.all().count()
    last_total_pregnancy = PregnancyReport.objects \
                                .filter(created_on__gte=period.start_on,
                                        created_on__lte=period.end_on) \
                                .count()
    print last_total_pregnancy, 'alou'
    context.update({'period': period, 
                    'total_children': total_children,
                    'last_total_children': last_total_children,
                    'total_pregnancy': total_pregnancy,
                    'last_total_pregnancy': last_total_pregnancy})
    print total_children, last_total_children


    return render(request, 'credos_dashboard.html', context)
