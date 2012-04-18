#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.shortcuts import render
from django.db.models import Q

from bolibana.models import Entity
from bolibana.web.decorators import provider_required
from unfpa_core.models import RHCommoditiesReport


@provider_required
def monthly_commodities(request, period):

    context = {'period': period}
    data = {}
    list_family_planning = RHCommoditiesReport.objects.filter(period=period, family_planning=True)
    data.update({"list_family_planning": list_family_planning})
    
    list_delivery_services = RHCommoditiesReport.objects.filter(period=period, delivery_services=True)
    data.update({"list_delivery_services": list_delivery_services})
    list_both_services = []
    list_both_services.extend(list_family_planning)
    list_both_services = [element for element in list_delivery_services if element in list_both_services]
    data.update({"list_both_services": list_both_services})

    val = -1
    query = (Q(male_condom=val) | Q(female_condom=val) | Q(oral_pills=val) | Q(injectable=val) |
             Q(iud=val) | Q(implants=val) | Q(female_sterilization=val) | Q(male_sterilization=val))

    stoct_out_methods = RHCommoditiesReport.objects.filter(query, period=period)
    print stoct_out_methods

    data.update({"stoct_out_methods": stoct_out_methods})

    context.update({'data': data})

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
