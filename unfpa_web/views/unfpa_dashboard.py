#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad

from django.shortcuts import render

from bolibana.web.decorators import provider_required
from unfpa_core.models import (RHCommoditiesReport, MaternalMortalityReport, 
                               ChildrenMortalityReport, UEntity)
from unfpa_web.views.data import current_period
from nosmsd.models import Inbox, SentItems



@provider_required
def unfpa_dashboard(request):
    context = {'category': 'unfpa', 'subcategory': 'unfpa_dashboard'}

    all_unfpa_center = UEntity.objects.filter(is_unfpa=True).all().count()
    context.update({"all_unfpa_center": all_unfpa_center})

    period = current_period()
    # message
    #/!\ Problème pour le unfpa seulement
    all_inbox = Inbox.objects.count()
    all_nb_entitems = SentItems.objects.count()

    context.update({"all_inbox": all_inbox, "all_nb_entitems": all_nb_entitems})

    nb_inbox = Inbox.objects.filter(receivingdatetime__gte=period.start_on,
                                    receivingdatetime__lte=period.end_on) \
                            .count()

    nb_entitems = SentItems.objects \
                           .filter(deliverydatetime__gte=period.start_on,
                                deliverydatetime__lte=period.end_on) \
                           .count()

    # Nombre decès enfants
    nb_death_children = ChildrenMortalityReport.periods.within(period).count()

    # Nombre decès femme enceints
    nb_death_Maternal = MaternalMortalityReport.periods.within(period).count()


    return render(request, 'unfpa_dashboard.html', context)
RHCommoditiesReport.objects.all().__len__()