#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad

from django.shortcuts import render

from bolibana.web.decorators import provider_required


@provider_required
def credos_dashboard(request):
    context = {'category': 'credos','subcategory': 'credos_dashboard'}

    return render(request, 'credos_dashboard.html', context)
