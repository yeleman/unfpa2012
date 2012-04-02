#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from bolibana.models import Entity, IndividualReport


class ChildrenMortalityReport(IndividualReport):

    YES = 'Y'
    NO = 'N'
    YESNO = ((YES, _(u"Yes")), (NO, _(u"No")))

    class Meta:
        app_label = 'unfpa_core'
        verbose_name = _(u"Children Mortality Report")
        verbose_name_plural = _(u"Children Mortality Reports")

    reporting_location = models.ForeignKey(Entity,
                                           related_name='children_reported_in',
                                          verbose_name=_(u"Reporting location"))
    name = models.CharField(max_length=100,
                            verbose_name=_(u"Name of the deceased"))
    dob = models.DateField(verbose_name=_(u"Date of birth"))
    dob_auto = models.BooleanField(default=False,
                                   verbose_name=_(u"DOB is an estimation?"))
    dod = models.DateField(verbose_name=_(u"Date of death"))
    death_location = models.ForeignKey(Entity, related_name='children_dead_in',
                                       verbose_name=_(u"Place of death"))

    def __unicode__(self):
        return ugettext(u"%(name)s/%(dod)s" 
                % {'name': self.name.title(),
                   'dod': self.dod.strftime('%d-%m-%Y')})


reversion.register(ChildrenMortalityReport)