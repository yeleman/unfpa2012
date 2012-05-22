#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.shortcuts import render
from django.db.models import Q

from bolibana.models import Entity
from bolibana.web.decorators import provider_required
from unfpa_core.models import RHCommoditiesReport



def check_planing_method(report):
    i = 0
    if report.male_condom != -1:
        i += 1
    if report.female_condom != -1:
        i += 1
    if report.oral_pills != -1:
        i += 1
    if report.injectable != -1:
        i += 1
    if report.iud != -1:
        i += 1
    if report.implants != -1:
        i += 1
    if report.female_sterilization == 'T':
        i += 1
    if report.male_sterilization == 'T':
        i += 1
    return i

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
             Q(iud=val) | Q(implants=val) | Q(female_sterilization='N') | Q(male_sterilization='N'))

    stoct_out_methods = RHCommoditiesReport.objects.filter(query, period=period)
    data.update({"stoct_out_methods": stoct_out_methods})

    all_reports = RHCommoditiesReport.objects.filter(period=period)
    last_tree_fp = 0
    for report in all_reports:
        if check_planing_method(report) >= 3:
            last_tree_fp += 1
    try:
        percent_last_tree_fp = (last_tree_fp * 100) / len(all_reports)
    except:
        percent_last_tree_fp = 0
    context.update({"last_tree_fp": last_tree_fp, 
                 "percent_last_tree_fp": percent_last_tree_fp})

    list_family_planning = RHCommoditiesReport.objects.filter(period=period, family_planning=True)
    data.update({"list_family_planning": list_family_planning})

    out_Oxytocin_Magnesium_Sulphate = RHCommoditiesReport.objects.filter((Q(oxytocine=val) | Q(magnesium_sulfate=val)), period=period)
    data.update({"out_Oxytocin_Magnesium_Sulphate": out_Oxytocin_Magnesium_Sulphate})
    
    dic = {}
    for entity in Entity.objects.all():
        reports_children = []  
        for child in entity.children.all():
            
            try:
                report = RHCommoditiesReport.objects.get(period=period, entity=child)
                print report
                reports_children.append(report)
            except:
                report = None
        print reports_children
        if reports_children:
            dic['%s' % entity]= reports_children

    context.update({"dic": dic})  

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
