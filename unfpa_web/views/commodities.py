#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import datetime

from django.shortcuts import render

from bolibana.models import MonthPeriod, QuarterPeriod, YearPeriod
from bolibana.web.decorators import provider_permission

from unfpa_core import unfpa_districts
from unfpa_core.models import RHCommoditiesReport


@provider_permission('can_view_indicator_data')
def monthly_commodities(request, period):

    context = {'period': period, 'category': 'unfpa',
               'subcategory': 'commodities'}

    rtypes = {MonthPeriod: 'monthly',
              QuarterPeriod: 'quarterly',
              YearPeriod: 'annual'}

    fp_services = RHCommoditiesReport.validated \
                                     .filter(period=period) \
                                     .filter(family_planning=True)

    delivery_services = RHCommoditiesReport.validated \
                                     .filter(period=period) \
                                     .filter(delivery_services=True)

    both_services = RHCommoditiesReport.validated \
                                     .filter(period=period) \
                                     .filter(delivery_services=True) \
                                     .filter(family_planning=True)

    fp_stockout = RHCommoditiesReport.objects.validated() \
                                     .has_stockouts().filter(period=period)

    atleast_3methods = sum([1
                        for report
                        in RHCommoditiesReport.validated.filter(period=period)
                        if report.fp_stockout_3methods()])
    try:
        atleast_3methods_percent = float(atleast_3methods) / \
                               RHCommoditiesReport.validated \
                                                  .filter(period=period).count()
    except ZeroDivisionError:
        atleast_3methods_percent = 0

    otoxycin_magnesium_stockout = RHCommoditiesReport.validated \
                                     .filter(period=period) \
                                     .filter(magnesium_sulfate=0) \
                                     .filter(oxytocine=0)

    context.update({'fp_services': (fp_services.count(), fp_services),
                    'delivery_services': (delivery_services.count(),
                                          delivery_services),
                    'both_services': (both_services.count(), both_services),
                    'fp_stockout': (fp_stockout.count(), fp_stockout),
                    'atleast_3methods': (atleast_3methods,
                                         atleast_3methods_percent),
                    'otoxycin_magnesium_stockout': (
                                            otoxycin_magnesium_stockout.count(),
                                            otoxycin_magnesium_stockout)})

    # districts
    all_stock_outs = []
    for district in unfpa_districts():
        centers = district.children \
                              .filter(type__slug__in=('cscom',
                                                      'csref', 'hospital'))
        nb_centers = float(centers.count())

        methods = ('male_condom', 'female_condom', 'oral_pills',
                           'injectable', 'iud', 'implants',
                           'female_sterilization', 'male_sterilization',
                           'magnesium_sulfate', 'oxytocine')
        stock_outs = {}
        for method in methods:
            stock_outs[method] = [0, 0]

        reports = RHCommoditiesReport.objects.validated().filter(period=period,
                                                       entity__in=centers)
        for report in reports:
            for method in methods:
                # increment counter of # of center with stockout.
                if getattr(report, method, report.SUPPLIES_NOT_PROVIDED) == 0:
                    stock_outs[method][0] += 1

        # compute percentages
        for key, method_so in stock_outs.items():
            try:
                stock_outs[key] = (method_so[0], method_so[0] / nb_centers)
            except ZeroDivisionError:
                pass

        all_stock_outs.append({'district': district,
                               'stock_outs': stock_outs,
                               'nb_centers': int(nb_centers),
                               'reports': reports})

    context.update({'all_stock_outs': all_stock_outs,
                    'type': rtypes.get(period.__class__, MonthPeriod)})

    return render(request, 'monthly_commodities.html', context)


def quarterly_annual_commodities(request, period, rtype):
    context = {'period': period, 'category': 'unfpa',
               'subcategory': 'commodities'}

    rtypes = {MonthPeriod: 'monthly',
              QuarterPeriod: 'quarterly',
              YearPeriod: 'annual'}

    our_periods = [month for month in period.months if month.end_on < datetime.now()]

    fp_services = [RHCommoditiesReport.validated \
                                      .filter(period=month) \
                                      .filter(family_planning=True).count()
                   for month in our_periods]

    delivery_services = [RHCommoditiesReport.validated \
                                            .filter(period=month) \
                                            .filter(delivery_services=True).count()
                         for month in our_periods]

    both_services = [RHCommoditiesReport.validated \
                                     .filter(period=month) \
                                     .filter(delivery_services=True) \
                                     .filter(family_planning=True).count()
                     for month in our_periods]

    fp_stockout = [RHCommoditiesReport.objects.validated() \
                                      .has_stockouts() \
                                      .filter(period=month).count()
                   for month in our_periods]

    atleast_3methods_t = []
    for month in our_periods:
        atleast_3methods = sum([1
                            for report
                            in RHCommoditiesReport.validated.filter(period=period)
                            if report.fp_stockout_3methods()])
        try:
            atleast_3methods_percent = float(atleast_3methods) / \
                                   RHCommoditiesReport.validated \
                                                      .filter(period=period).count()
        except ZeroDivisionError:
            atleast_3methods_percent = 0
        atleast_3methods_t.append((atleast_3methods, atleast_3methods_percent))

    otoxycin_magnesium_stockout = [RHCommoditiesReport.validated \
                                     .filter(period=month) \
                                     .filter(magnesium_sulfate=0) \
                                     .filter(oxytocine=0).count()
                                   for month in our_periods]

    context.update({'fp_services': fp_services,
                    'delivery_services': delivery_services,
                    'both_services': both_services,
                    'fp_stockout': fp_stockout,
                    'atleast_3methods': atleast_3methods_t,
                    'otoxycin_magnesium_stockout':otoxycin_magnesium_stockout})


    # districts
    all_stock_outs = []
    for district in unfpa_districts():
        centers = district.children \
                          .filter(type__slug__in=('cscom',
                                                  'csref', 'hospital'))
        nb_centers = float(centers.count())

        methods = ('male_condom', 'female_condom', 'oral_pills',
                           'injectable', 'iud', 'implants',
                           'female_sterilization', 'male_sterilization',
                           'magnesium_sulfate', 'oxytocine')

        month_stock_outs = []
        for month in our_periods:

            stock_outs = {}
            for method in methods:
                stock_outs[method] = [0, 0]

            reports = RHCommoditiesReport.objects.validated().filter(period=month,
                                                                 entity__in=centers)
            for report in reports:
                for method in methods:
                    # increment counter of # of center with stockout.
                    if getattr(report, method, report.SUPPLIES_NOT_PROVIDED) == 0:
                        stock_outs[method][0] += 1

            # compute percentages
            for key, method_so in stock_outs.items():
                try:
                    stock_outs[key] = (method_so[0], method_so[0] / nb_centers)
                except ZeroDivisionError:
                    pass

            stock_outs.update({'month': month})
            month_stock_outs.append(stock_outs)

        all_stock_outs.append({'district': district,
                               'stock_outs': month_stock_outs,
                               'nb_centers': int(nb_centers),
                               'reports': reports})

    context.update({'all_stock_outs': all_stock_outs,})

    context.update({'type': rtypes.get(period.__class__, MonthPeriod),
                    'our_periods': our_periods})

    return render(request, 'quarterly_annual_commodities.html', context)



@provider_permission('can_view_indicator_data')
def quarterly_commodities(request, period):
    return quarterly_annual_commodities(request, period, 'quarterly')


@provider_permission('can_view_indicator_data')
def annual_commodities(request, period):
    return quarterly_annual_commodities(request, period, 'annual')
