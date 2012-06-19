#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from django.core.management.base import BaseCommand
from django.contrib.auth.models import ContentType

from datetime import date, datetime

from bolibana.models import MonthPeriod, YearPeriod

from unfpa_core.models import (MaternalMortalityReport,
                               ChildrenMortalityReport,
                               PregnancyReport,
                               BirthReport,
                               RHCommoditiesReport)


class Command(BaseCommand):

    def handle(self, *args, **options):

        current_period = MonthPeriod.find_create_by_date(date.today())

        now = datetime.now()

        # find our date of first report (begining of activities)
        first_report = date.today()
        try:
            child = ChildrenMortalityReport.objects.all().order_by('dod')[0].dod
        except:
            child = None
        try:
            mat = MaternalMortalityReport.objects.all().order_by('dod')[0].dod
        except:
            mat = None
        try: 
            preg = PregnancyReport.objects.all().order_by('creatd_on')[0].creatd_on
        except:
            preg = None
        try: 
            bir = BirthReport.objects.all().order_by('creatd_on')[0].created_on
        except:
            bir = None
        try: 
            commod = RHCommoditiesReport.objects.all().order_by('period')[0].period.start_on
            commod = date(commod.year, commod.month, commod.day)
        except:
            commod = None
        if child:
            first_report = child
        if mat and mat < first_report:
            first_report = mat
        if preg and preg < first_report:
            first_report = preg
        if bir and bir < first_report:
            first_report = bir
        if commod and commod < first_report:
            first_report = commod

        first_period = MonthPeriod.find_create_by_date(first_report)

        for year in range(first_period.start_on.year, current_period.end_on.year + 1):

            # create year
            y = YearPeriod.find_create_from(year)
            print(y)

            # create quarter
            for quarter in y.quarters_:
                if quarter.start_on > now:
                    break
                quarter.save()
                print(u"\t%s" % quarter)

            # create months:
            for month in y.months:
                if month.start_on > now:
                    break
                month.save()
                print(u"\t\t%s" % month)

                # create weeks
                for week in month.weeks:
                    if week.start_on > now:
                       break
                    week.save()
                    print(u"\t\t\t%s" % week)
