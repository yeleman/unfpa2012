#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.shortcuts import render

from bolibana.web.decorators import provider_required



@provider_required
def unfpa_dashboard(request):
    context = {'category': 'unfpa_dashboard'}

    return render(request, 'unfpa_dashboard.html', context)
