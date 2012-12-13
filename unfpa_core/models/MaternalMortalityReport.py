#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from bolibana.models import Entity, IndividualReport, Report


class PeriodManager(models.Manager):

    def get_query_set(self):
        return super(PeriodManager, self).get_query_set()

    def within(self, period=None):
        if not period:
            return self.get_query_set()
        else:
            return self.get_query_set().filter(dod__gte=period.start_on,
                                               dod__lte=period.end_on)


class MaternalMortalityReport(IndividualReport):

    UNFPA = 'U'
    CREDOS = 'C'
    SOURCES = ((UNFPA, u"UNFPA"),
               (CREDOS, u"CREDOS"))

    CAUSE_BLEEDING = 'b'
    CAUSE_FEVER = 'f'
    CAUSE_HTN = 'h'
    CAUSE_DIARRHEA = 'd'
    CAUSE_CRISIS = 'c'
    CAUSE_MISCARRIAGE = 'm'
    CAUSE_ABORTION = 'a'
    CAUSE_OTHER = 'o'
    DEATH_CAUSES_t = ((CAUSE_BLEEDING, u"Bleeding"),
                    (CAUSE_FEVER, u"Fever"),
                    (CAUSE_HTN, u"High Blood Pressure"),
                    (CAUSE_DIARRHEA, u"Diarrhea"),
                    (CAUSE_CRISIS, u"Crisis"),
                    (CAUSE_MISCARRIAGE, u"Miscarriage"),
                    (CAUSE_ABORTION, u"Abortion"),
                    (CAUSE_OTHER, u"Other"))
    DEATH_CAUSES = {
                    CAUSE_BLEEDING: u"Bleeding",
                    CAUSE_FEVER: u"Fever",
                    CAUSE_HTN: u"High Blood Pressure",
                    CAUSE_DIARRHEA: u"Diarrhea",
                    CAUSE_CRISIS: u"Crisis",
                    CAUSE_MISCARRIAGE: u"Miscarriage",
                    CAUSE_ABORTION: u"Abortion",
                    CAUSE_OTHER: u"Other"}

    class Meta:
        app_label = 'unfpa_core'
        verbose_name = _(u"Maternal Mortality Report")
        verbose_name_plural = _(u"Maternal Mortality Reports")

    reporting_location = models.ForeignKey(Entity,
                                           related_name='maternal_reported_in',
                                           verbose_name=_(u"Reporting "
                                                          u"location"))
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
                                                 u"children of the deceased"))
    dead_children = models.PositiveIntegerField(verbose_name=_(u"Dead children"
                                                u" of the deceased"))
    pregnant = models.BooleanField(verbose_name=_(u"Pregnant?"))
    pregnancy_weeks = models.PositiveIntegerField(null=True, blank=True,
                                                  verbose_name=_(u"Duration "
                                                  u"of the pregnancy (weeks)"))
    pregnancy_related_death = models.BooleanField(default=False,
                                                  verbose_name=_(u"Pregnancy "
                                                  u"related death"))

    cause_of_death = models.CharField(max_length=1, choices=DEATH_CAUSES_t)

    source = models.CharField(max_length=1, null=True,
                              blank=True, choices=SOURCES)

    # django manager first
    objects = models.Manager()
    periods = PeriodManager()

    def __unicode__(self):
        return ugettext(u"%(name)s/%(dod)s"
                        % {'name': self.name.title(),
                           'dod': self.dod.strftime('%d-%m-%Y')})


reversion.register(MaternalMortalityReport)


class AggregatedMaternalMortalityReport(Report):

    class Meta:
        app_label = 'unfpa_core'
        verbose_name = _(u"Aggregated Maternal Mortality Report")
        verbose_name_plural = _(u"Aggregated Maternal Mortality Reports")

    age_under_15 = models.IntegerField()
    age_under_18 = models.IntegerField()
    age_under_20 = models.IntegerField()
    age_under_25 = models.IntegerField()
    age_under_30 = models.IntegerField()
    age_under_35 = models.IntegerField()
    age_under_40 = models.IntegerField()
    age_under_45 = models.IntegerField()
    age_under_50 = models.IntegerField()
    age_over_50 = models.IntegerField()

    have_living_children = models.IntegerField()
    have_dead_children = models.IntegerField()

    is_pregnant = models.IntegerField()
    is_pregnant_1month = models.IntegerField()
    is_pregnant_2month = models.IntegerField()

    is_pregnancy_related = models.IntegerField()

    cause_bleeding = models.IntegerField()
    cause_fever = models.IntegerField()
    cause_htn = models.IntegerField()
    cause_diarrhea = models.IntegerField()
    cause_crisis = models.IntegerField()
    cause_miscarriage = models.IntegerField()
    cause_abortion = models.IntegerField()
    cause_other = models.IntegerField()

    indiv_sources = models.ManyToManyField('MaternalMortalityReport',
                                           verbose_name=_(u"Indiv. Sources"),
                                           blank=True, null=True)

    agg_sources = models.ManyToManyField('MaternalMortalityReport',
                                         verbose_name=_(u"Aggr. Sources"),
                                         blank=True, null=True)

    @classmethod
    def create_from(cls, period, entity, author):

        # create empty
        agg_report = cls.init_empty(entity, period, author)

        # find list of sources
        indiv_sources = MaternalMortalityReport \
                            .objects \
                            .filter(dod__gte=period.start_on,
                                    dod__lte=period.end_on,
                                    death_location__in=entity.get_children())
        agg_sources = cls.objects.filter(period=period,
                                         entity__in=entity.get_children())

        sources = list(indiv_sources) + list(agg_sources)

        # loop on all sources
        for source in sources:
            if isinstance(source, MaternalMortalityReport):
                cls.update_instance_with_indiv(agg_report, source)
            elif isinstance(source, cls):
                cls.update_instance_with_agg(agg_report, source)

        # keep a record of all sources
        for report in indiv_sources:
            agg_report.indiv_sources.add(report)

        for report in agg_sources:
            agg_report.agg_sources.add(report)

        with reversion.create_revision():
            agg_report.save()
            reversion.set_user(author.user)

        return agg_report

    @classmethod
    def update_instance_with_indiv(cls, report, instance):

        # sex
        if instance.sex == instance.MALE:
            report.sex_male += 1
        elif instance.sex == instance.FEMALE:
            report.sexe_female += 1

        # death place
        if instance.death_place == instance.HOME:
            report.death_home += 1
        elif instance.death_place == instance.CENTER:
            report.death_center += 1
        else:
            report.death_other += 1

        # cause of death
        if instance.cause_of_death == instance.CAUSE_FEVER:
            report.cause_death_fever += 1
        elif instance.cause_of_death == instance.CAUSE_DIARRHEA:
            report.cause_death_diarrhea += 1
        elif instance.cause_of_death == instance.CAUSE_DYSPNEA:
            report.cause_death_dyspnea += 1
        elif instance.cause_of_death == instance.CAUSE_ANEMIA:
            report.cause_death_anemia += 1
        elif instance.cause_of_death == instance.CAUSE_RASH:
            report.cause_death_rash += 1
        elif instance.cause_of_death == instance.CAUSE_COUGH:
            report.cause_death_cough += 1
        elif instance.cause_of_death == instance.CAUSE_VOMITING:
            report.cause_death_vomiting += 1
        elif instance.cause_of_death == instance.CAUSE_NUCHAL_RIGIDITY:
            report.cause_death_nuchal_rigidity += 1
        elif instance.cause_of_death == instance.CAUSE_RED_EYE:
            report.cause_death_red_eye += 1
        elif instance.cause_of_death == instance.CAUSE_EAT_REFUSAL:
            report.cause_death_eat_refusal += 1
        else:
            report.cause_death_other += 1

        # age
        age_days = (instance.dod - instance.dod).days
        if age_days < 7:
            report.age_under_1w += 1
        if age_days < 14:
            report.age_under_2weeks += 1
        if age_days < 30:
            report.age_under_1month += 1
        if age_days / 30 < 3:
            report.age_under_3month += 1
        if age_days / 30 < 6:
            report.age_under_6month += 1
        if age_days / 30 < 9:
            report.age_under_9month += 1
        if age_days < 365:
            report.age_under_1 += 1
        if age_days / 365 < 2:
            report.age_under_2 += 1
        if age_days / 365 < 3:
            report.age_under_3 += 1
        if age_days / 365 < 4:
            report.age_under_4 += 1
        if age_days / 365 <= 5:
            report.age_under_5 += 1

    @classmethod
    def update_instance_with_agg(cls, report, instance):

        report.sex_male += instance.sex_male
        report.sexe_female += instance.sexe_female

        report.age_under_1w += instance.age_under_1w
        report.age_under_2weeks += instance.age_under_2weeks
        report.age_under_1month += instance.age_under_1month
        report.age_under_3month += instance.age_under_3month
        report.age_under_6month += instance.age_under_6month
        report.age_under_9month += instance.age_under_9month
        report.age_under_1 += instance.age_under_1
        report.age_under_2 += instance.age_under_2
        report.age_under_3 += instance.age_under_3
        report.age_under_4 += instance.age_under_4
        report.age_under_5 += instance.age_under_5

        report.death_home += instance.death_home
        report.death_center += instance.death_center
        report.death_other += instance.death_other

        report.cause_death_fever += instance.cause_death_fever
        report.cause_death_diarrhea += instance.cause_death_diarrhea
        report.cause_death_dyspnea += instance.cause_death_dyspnea
        report.cause_death_anemia += instance.cause_death_anemia
        report.cause_death_rash += instance.cause_death_rash
        report.cause_death_cough += instance.cause_death_cough
        report.cause_death_vomiting += instance.cause_death_vomiting
        report.cause_death_nuchal_rigidity += \
                                           instance.cause_death_nuchal_rigidity
        report.cause_death_red_eye += instance.cause_death_red_eye
        report.cause_death_eat_refusal += instance.cause_death_eat_refusal
        report.cause_death_other += instance.cause_death_other
