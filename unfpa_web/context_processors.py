#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import date

from bolibana.models import MonthPeriod


def add_last_period(request):
    """ Add the last period string """

    last_period = MonthPeriod.find_create_by_date(date.today()).previous().middle().strftime('%m-%Y')
    return {'last_period': last_period}


def add_all_periods(request):

    if not 'unfpa' in request.path:
        return {}

    from datetime import date
    from bolibana.models import WeekPeriod, MonthPeriod, QuarterPeriod, YearPeriod
    now = date.today()

    return {'allperiods': 
        {'weeks': WeekPeriod.objects.filter(start_on__lte=now),
         'months': MonthPeriod.objects.filter(start_on__lte=now),
         'quarters': QuarterPeriod.objects.filter(start_on__lte=now),
         'years': YearPeriod.objects.filter(start_on__lte=now)}}