#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import date

from django.http import Http404

from bolibana.models import (MonthPeriod, WeekPeriod,
                             QuarterPeriod, YearPeriod)
from bolibana.web.decorators import provider_required



def import_path(name):
    """ import a callable from full module.callable name """
    modname, _, attr = name.rpartition('.')
    if not modname:
        # single module name
        return __import__(attr)
    m = __import__(modname, fromlist=[attr])
    return getattr(m, attr)


@provider_required
def report_chooser(request, report_type, period_type, period_str=None):

    if not report_type in ('children', 'maternal', 'commodities'):
        raise Http404(u"Invalid report type")

    if (not period_type in ('monthly', 'annual', 'quarterly', 'weekly')
        or (report_type == 'commodities' and period_type == 'weekly')):
        raise Http404(u"Invalid period type")

    try:
        view = import_path('unfpa_web.views.%(report_type)s.'
                           '%(period_type)s_%(report_type)s'
                           % {'report_type': report_type,
                              'period_type': period_type})
    except:
        raise
        raise Http404(u"Incorrect URL.")

    try:
        if '-' in period_str:
            indice, year = period_str.split('-')
            indice = int(indice)
            year = int(year)
        else:
            indice = None
            year = int(period_str)
    except:
        raise Http404(u"Incorrect period.")

    if period_type == 'weekly':
        period = WeekPeriod.find_create_by_weeknum(year, indice)
    elif period_type == 'monthly':
        period = MonthPeriod.find_create_from(year, month=indice)
    elif period_type == 'quarterly':
        period = QuarterPeriod.find_create_by_quarter(year, indice)
    elif period_type == 'annual':
        period = YearPeriod.find_create_from(year)
    else:
        # default period is current Month
        period = MonthPeriod.find_create_by_date(date.today())

    return view(request, period)