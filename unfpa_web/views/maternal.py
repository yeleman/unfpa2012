#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.shortcuts import render
from django.http import HttpResponse

from bolibana.models import Entity
from bolibana.web.decorators import provider_permission

from unfpa_core.models import MaternalMortalityReport
from unfpa_core.exports import maternal_as_excel


def weekly_monthly_maternal(request, period, rtype):
    context = {'period': period, 'category': 'unfpa',
               'subcategory': 'maternal'}
    data = []
    for district in Entity.objects.filter(type__slug='district'):
        nb_deaths = MaternalMortalityReport.periods.within(period) \
                       .filter(pregnancy_related_death=True) \
                       .filter(death_location__in=district.get_descendants()) \
                       .filter(source=MaternalMortalityReport.UNFPA) \
                       .count()
        data.append({'district': district, 'deaths': nb_deaths})

    context.update({'data': data, 'type': rtype})

    return render(request, 'weekly_monthly_maternal.html', context)


@provider_permission('can_view_indicator_data')
def weekly_maternal(request, period):
    return weekly_monthly_maternal(request, period, 'weekly')


@provider_permission('can_view_indicator_data')
def monthly_maternal(request, period):
    return weekly_monthly_maternal(request, period, 'monthly')


def quarterly_annual_maternal(request, period, rtype):
    context = {'period': period, 'category': 'unfpa',
               'subcategory': 'maternal'}
    data = []
    months = period.months

    # total deaths for all districts
    # /!\ UNFPA districts only
    all_deaths = MaternalMortalityReport.periods.within(period) \
                           .filter(pregnancy_related_death=True) \
                           .filter(source=MaternalMortalityReport.UNFPA) \
                           .count()

    # for each district
    for district in Entity.objects.filter(type__slug='district'):
        mdeaths = []
        for month in months:
            nb_deaths = MaternalMortalityReport.periods.within(month) \
                           .filter(pregnancy_related_death=True) \
                           .filter(death_location__in=district
                                   .get_descendants()) \
                           .filter(source=MaternalMortalityReport.UNFPA) \
                           .count()
            mdeaths.append(nb_deaths)
        total = sum(mdeaths)
        try:
            percent = float(total) / all_deaths
        except ZeroDivisionError:
            percent = 0
        data.append({'district': district, 'mdeaths': mdeaths,
                     'total': total, 'all_deaths': all_deaths,
                     'percent_of_all': percent})

    context.update({'data': data, 'type': rtype, 'months': months})

    return render(request, 'quarterly_annual_maternal.html', context)


@provider_permission('can_view_indicator_data')
def quarterly_maternal(request, period):
    return quarterly_annual_maternal(request, period, 'quarterly')


@provider_permission('can_view_indicator_data')
def annual_maternal(request, period):
    return quarterly_annual_maternal(request, period, 'annual')

############### export xls #################


def weekly_monthly_maternal_export(request, period, rtype):
    """ """

    data = []
    for district in Entity.objects.filter(type__slug='district'):
        nb_deaths = MaternalMortalityReport.periods.within(period) \
                       .filter(pregnancy_related_death=True) \
                       .filter(death_location__in=district.get_descendants()) \
                       .filter(source=MaternalMortalityReport.UNFPA) \
                       .count()
        data.append({'district': district, 'deaths': nb_deaths})

    file_name = 'Rapports de mortalite maternelle.xls'

    file_content = maternal_as_excel(data, period).getvalue()

    response = HttpResponse(file_content, \
                            content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    response['Content-Length'] = len(file_content)

    return response


@provider_permission('can_view_indicator_data')
def weekly_maternal_export(request, period):
    return weekly_monthly_maternal_export(request, period, 'weekly')


@provider_permission('can_view_indicator_data')
def monthly_maternal_export(request, period):
    return weekly_monthly_maternal_export(request, period, 'monthly')


def quarterly_annual_maternal_export(request, period, rtype):
    """   """

    data = []
    months = period.months

    # total deaths for all districts
    # /!\ UNFPA districts only
    all_deaths = MaternalMortalityReport.periods.within(period) \
                           .filter(pregnancy_related_death=True) \
                           .filter(source=MaternalMortalityReport.UNFPA) \
                           .count()

    # for each district
    for district in Entity.objects.filter(type__slug='district'):
        mdeaths = []
        for month in months:
            nb_deaths = MaternalMortalityReport.periods.within(month) \
                           .filter(pregnancy_related_death=True) \
                           .filter(death_location__in=district
                                   .get_descendants()) \
                           .filter(source=MaternalMortalityReport.UNFPA) \
                           .count()
            mdeaths.append(nb_deaths)
        total = sum(mdeaths)
        try:
            percent = float(total) / all_deaths
        except ZeroDivisionError:
            percent = 0
        data.append({'district': district, 'mdeaths': mdeaths,
                     'total': total, 'all_deaths': all_deaths,
                     'percent_of_all': percent})

    file_name = 'Rapports de mortalite maternelle.xls'

    file_content = maternal_as_excel(data, period).getvalue()

    response = HttpResponse(file_content, \
                            content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    response['Content-Length'] = len(file_content)

    return response


@provider_permission('can_view_indicator_data')
def quarterly_maternal_export(request, period):
    return quarterly_annual_maternal_export(request, period, 'quarterly')


@provider_permission('can_view_indicator_data')
def annual_maternal_export(request, period):
    return quarterly_annual_maternal_export(request, period, 'annual')
