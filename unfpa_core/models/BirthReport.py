#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from bolibana.models import Entity, IndividualReport


class BirthReport(IndividualReport):

    YES = 'Y'
    NO = 'N'
    YESNO = ((YES, _(u"Yes")), (NO, _(u"No")))

    HOME = "D"
    CENTER = "C"
    OTHER = "A"
    PLACEBIRTH = ((HOME, _(u"Home")),
                  (CENTER, _(u"Center")),
                  (OTHER, _(u"Other")))

    MAL = 'M'
    FEMALE = 'F'
    SEX = ((FEMALE, _(u"F")), (MAL, _(u"M")))

    class Meta:
        app_label = 'unfpa_core'
        verbose_name = _(u"Birth Report")
        verbose_name_plural = _(u"Birth Reports")

    reporting_location = models.ForeignKey(Entity,
                                         related_name='birth_reported_in',
                                         verbose_name=_(u"Reporting location"))
    name_householder = models.CharField(max_length=100,
                            verbose_name=_(u"Householder"))
    name_father = models.CharField(max_length=100,
                            verbose_name=_(u"Name of father"))
    name_mother = models.CharField(max_length=100,
                            verbose_name=_(u"Name of mother"))
    name_child = models.CharField(max_length=100,
                            verbose_name=_(u"Name of child"))

    sex = models.CharField(max_length=1,
                                   choices=SEX,
                                   verbose_name=_(u"Sex"))
    dob = models.DateField(verbose_name=_(u"Date of birth"))
    dob_auto = models.BooleanField(default=False,
                                   verbose_name=_(u"DOB is an estimation?"))
    born_alive = models.CharField(max_length=1,
                                   choices=YESNO,
                                   verbose_name=_(u"Born alive"))
    birth_location = models.CharField(max_length=1,
                                   choices=PLACEBIRTH,
                                   verbose_name=_(u"Place of birth"))
    other = models.CharField(max_length=100, blank=True, null=True,
                            verbose_name=_(u"Autre"))

    def __unicode__(self):
        return ugettext(u"%(name_child)s/%(dob)s" 
                % {'name_child': self.name_child.title(),
                   'dob': self.dob.strftime('%d-%m-%Y')})


reversion.register(BirthReport)
