#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.shortcuts import render

from bolibana.models import Entity
from bolibana.web.decorators import provider_required

from unfpa_core import unfpa_districts
from unfpa_core.models import RHCommoditiesReport


@provider_required
def monthly_commodities(request, period):

    context = {'period': period}
    
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
                                     .has_stockout().filter(period=period)

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
        print(all_stock_outs)

    context.update({'all_stock_outs': all_stock_outs})

    return render(request, 'monthly_commodities.html', context)


@provider_required
def quarterly_commodities(request, period):

    context = {'period': period}
    data = []
    for district in Entity.objects.filter(type__slug='district'):
        nb_deaths = 0
        data.append({'district': district, 'deaths': nb_deaths})

    context.update({'data': data})

    return render(request, 'quarterly_commodities.html', context)


@provider_required
def annual_commodities(request, period):

    context = {'period': period}
    data = []
    for district in Entity.objects.filter(type__slug='district'):
        nb_deaths = 0
        data.append({'district': district, 'deaths': nb_deaths})

    context.update({'data': data})

    return render(request, 'annual_commodities.html', context)
