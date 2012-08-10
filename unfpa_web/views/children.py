#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.shortcuts import render
from django.http import HttpResponse

from bolibana.models import Entity
from bolibana.web.decorators import provider_permission

from unfpa_core.models import ChildrenMortalityReport
from unfpa_core.exports import children_as_excel


def weekly_monthly_children(request, period, rtype):
    context = {'period': period, 'category': 'unfpa',
               'subcategory': 'children'}
    data = []
    for district in Entity.objects.filter(type__slug='district'):
        nb_deaths = ChildrenMortalityReport.periods.within(period) \
                       .filter(death_location__in=district.get_descendants()) \
                       .filter(source=ChildrenMortalityReport.UNFPA) \
                       .count()
        data.append({'district': district, 'deaths': nb_deaths})

    context.update({'data': data, 'type': rtype})

    return render(request, 'weekly_monthly_children.html', context)


@provider_permission('can_view_indicator_data')
def weekly_children(request, period):
    return weekly_monthly_children(request, period, 'weekly')


@provider_permission('can_view_indicator_data')
def monthly_children(request, period):
    return weekly_monthly_children(request, period, 'monthly')


def quarterly_annual_children(request, period, rtype):
    context = {'period': period, 'category': 'unfpa',
               'subcategory': 'children'}
    data = []
    months = period.months

    # total deaths for all districts
    # /!\ UNFPA districts only
    all_deaths = ChildrenMortalityReport.periods.within(period) \
                                .filter(source=ChildrenMortalityReport.UNFPA) \
                                .count()

    # for each district
    for district in Entity.objects.filter(type__slug='district'):
        mdeaths = []
        for month in months:
            nb_deaths = ChildrenMortalityReport.periods.within(month) \
                           .filter(death_location__in=district
                                   .get_descendants()) \
                           .filter(source=ChildrenMortalityReport.UNFPA) \
                           .count()
            mdeaths.append(nb_deaths)
        total = sum(mdeaths)

        try:
            percent_of_all = float(total) / all_deaths
        except ZeroDivisionError:
            percent_of_all = 0
        data.append({'district': district, 'mdeaths': mdeaths,
                     'total': total, 'all_deaths': all_deaths,
                     'percent_of_all': percent_of_all})

    context.update({'data': data, 'type': rtype, 'months': months})

    return render(request, 'quarterly_annual_children.html', context)


@provider_permission('can_view_indicator_data')
def quarterly_children(request, period):
    return quarterly_annual_children(request, period, 'quarterly')


@provider_permission('can_view_indicator_data')
def annual_children(request, period):
    return quarterly_annual_children(request, period, 'annual')


##########" exports"


def weekly_monthly_children_export(request, period, rtype):
    context = {'period': period, 'category': 'unfpa',
               'subcategory': 'children'}
    data = []
    for district in Entity.objects.filter(type__slug='district'):
        nb_deaths = ChildrenMortalityReport.periods.within(period) \
                       .filter(death_location__in=district.get_descendants()) \
                       .filter(source=ChildrenMortalityReport.UNFPA) \
                       .count()
        data.append({'district': district, 'deaths': nb_deaths})

    context.update({'data': data, 'type': rtype})

    #return render(request, 'weekly_monthly_children.html', context)

    file_name = 'Rapports mensuels de children.xls'

    file_content = children_as_excel(data, period).getvalue()

    response = HttpResponse(file_content, \
                            content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    response['Content-Length'] = len(file_content)

    return response


@provider_permission('can_view_indicator_data')
def weekly_children_export(request, period):
    return weekly_monthly_children_export(request, period, 'weekly')


@provider_permission('can_view_indicator_data')
def monthly_children_export(request, period):
    return weekly_monthly_children_export(request, period, 'monthly')


def quarterly_annual_children_export(request, period, rtype):
    context = {'period': period, 'category': 'unfpa',
               'subcategory': 'children'}
    data = []
    months = period.months

    # total deaths for all districts
    # /!\ UNFPA districts only
    all_deaths = ChildrenMortalityReport.periods.within(period) \
                                .filter(source=ChildrenMortalityReport.UNFPA) \
                                .count()

    # for each district
    for district in Entity.objects.filter(type__slug='district'):
        mdeaths = []
        for month in months:
            nb_deaths = ChildrenMortalityReport.periods.within(month) \
                           .filter(death_location__in=district
                                   .get_descendants()) \
                           .filter(source=ChildrenMortalityReport.UNFPA) \
                           .count()
            mdeaths.append(nb_deaths)
        total = sum(mdeaths)

        try:
            percent_of_all = float(total) / all_deaths
        except ZeroDivisionError:
            percent_of_all = 0
        data.append({'district': district, 'mdeaths': mdeaths,
                     'total': total, 'all_deaths': all_deaths,
                     'percent_of_all': percent_of_all})

    context.update({'data': data, 'type': rtype, 'months': months})

    file_name = 'Rapports mensuels de children.xls'

    file_content = children_as_excel(data, period).getvalue()

    response = HttpResponse(file_content, \
                            content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    response['Content-Length'] = len(file_content)

    return response

@provider_permission('can_view_indicator_data')
def quarterly_children_export(request, period):
    return quarterly_annual_children_export(request, period, 'quarterly')


@provider_permission('can_view_indicator_data')
def annual_children_export(request, period):
    return quarterly_annual_children_export(request, period, 'annual')