#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.shortcuts import render

from bolibana.models import Entity
from bolibana.web.decorators import provider_required


@provider_required
def weekly_maternal(request, period):

    context = {'period': period}
    data = []
    for district in Entity.objects.filter(type__slug='district'):
        nb_deaths = 0
        data.append({'district': district, 'deaths': nb_deaths})

    context.update({'data': data})

    return render(request, 'weekly_maternal.html', context)

@provider_required
def monthly_maternal(request, period):

    context = {'period': period}
    data = []
    for district in Entity.objects.filter(type__slug='district'):
        nb_deaths = 0
        data.append({'district': district, 'deaths': nb_deaths})

    context.update({'data': data})

    return render(request, 'monthly_maternal.html', context)


@provider_required
def quarterly_maternal(request, period):

    context = {'period': period}
    data = []
    for district in Entity.objects.filter(type__slug='district'):
        nb_deaths = 0
        data.append({'district': district, 'deaths': nb_deaths})

    context.update({'data': data})

    return render(request, 'quarterly_maternal.html', context)


@provider_required
def annual_maternal(request, period):

    context = {'period': period}
    data = []
    for district in Entity.objects.filter(type__slug='district'):
        nb_deaths = 0
        data.append({'district': district, 'deaths': nb_deaths})

    context.update({'data': data})

    return render(request, 'annual_maternal.html', context)
