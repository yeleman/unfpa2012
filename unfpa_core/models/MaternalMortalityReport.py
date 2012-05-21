#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from bolibana.models import Entity, IndividualReport


class MaternalMortalityReport(IndividualReport):

    class Meta:
        app_label = 'unfpa_core'
        verbose_name = _(u"Maternal Mortality Report")
        verbose_name_plural = _(u"Maternal Mortality Reports")

    reporting_location = models.ForeignKey(Entity,
                                           related_name='maternal_reported_in',
                                           verbose_name=_(u"Reporting location"))
    name = models.CharField(max_length=100,
                            verbose_name=_(u"Name of the deceased"))
    dob = models.DateField(verbose_name=_(u"Date of birth"))
    dob_auto = models.BooleanField(default=False,
                                   verbose_name=_(u"DOB is an estimation?"))
    dod = models.DateField(verbose_name=_(u"Date of death"))
    death_location = models.ForeignKey(Entity,
                                       related_name='maternal_dead_in',
                                       verbose_name=_(u"Place of death"))
    living_children = models.PositiveIntegerField(verbose_name=_(u"Living "
                                                                 u"children of"
                                                                 u" the deceased"))
    dead_children = models.PositiveIntegerField(verbose_name=_(u"Dead children "
                                                               u"of the deceased"))
    pregnant = models.BooleanField(verbose_name=_(u"Pregnant?"))
    pregnancy_weeks = models.PositiveIntegerField(null=True, blank=True,
                                                  verbose_name=_(u"Duration "
                                                                 u"of the pregnancy"
                                                                 u" (weeks)"))
    pregnancy_related_death = models.BooleanField(default=False,
                                                  verbose_name=_(u"Pregnancy "
                                                                 u"related death"))

    def __unicode__(self):
        return ugettext(u"%(name)s/%(dod)s" 
                        % {'name': self.name.title(),
                           'dod': self.dod.strftime('%d-%m-%Y')})


reversion.register(MaternalMortalityReport)
