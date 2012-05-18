#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from bolibana.models import Entity, IndividualReport


class PregnancyReport(IndividualReport):

    NONE = 0
    ALIVE = 1
    STILLBORN = 2
    ABORTION = 3

    RESULT = ((NONE, "None"), \
              (ALIVE, "Né vivant"), \
              (STILLBORN, "Mort-né"), \
              (ABORTION, "Avortement"))

    MAL = 'M'
    FEMALE = 'F'

    class Meta:
        app_label = 'unfpa_core'
        verbose_name = _(u"Pregnancy Report")
        verbose_name_plural = _(u"Pregnancy Reports")

    reporting_location = models.ForeignKey(Entity,
                                         related_name='pregnancy_reported_in',
                                         verbose_name=_(u"Reporting location"))
    name_householder = models.CharField(max_length=100,
                            verbose_name=_(u"Householder"))
    name_woman = models.CharField(max_length=100,
                            verbose_name=_(u"Name of woman"))

    dob = models.DateField(verbose_name=_(u"Date of birth"))
    dob_auto = models.BooleanField(default=False,
                                   verbose_name=_(u"DOB is an estimation?"))
    age_pregnancy = models.IntegerField(max_length=2,
                                   verbose_name=_(u"Age of pregnancy"))
    expected_date_confinement = models.DateField( \
                                verbose_name=_(u"Expected date confinement"))
    date_pregnancy = models.DateField(blank=True, null=True, \
                                verbose_name=_(u"Date pregnancy"))
    result_pregnancy = models.CharField(max_length=1,
                                   choices=RESULT,
                                   verbose_name=_(u"Resulting pregnancy"))

    def __unicode__(self):
        return ugettext(u"%(name_woman)s/%(dob)s"
                % {'name_woman': self.name_woman.title(),
                   'dob': self.dob.strftime('%d-%m-%Y')})


reversion.register(PregnancyReport)
