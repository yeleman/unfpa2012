#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from bolibana.models import Entity


class UEntity(Entity):

    class Meta:
        app_label = 'unfpa_core'
        verbose_name = _(u"U Entity")
        verbose_name_plural = _(u"U Entities")

    is_unfpa = models.BooleanField(default=False,
                                   verbose_name=_(u"FNUAP"))
    is_credos = models.BooleanField(default=False,
                                       verbose_name=_(u"CREDOS"))

    def __unicode__(self):
        return ugettext(u"%(name)s"
                % {'name': self.name.title()})


reversion.register(UEntity)