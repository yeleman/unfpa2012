#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import re

from datetime import date, timedelta

from unfpa_core.models import MaternalMortalityReport, ChildrenMortalityReport
from bolibana.models import Entity, Provider


def resp_error(message, action):
    message.respond(u"[ERREUR] Impossible de comprendre le SMS pour %s"
                                                               % action)
    return True


def resp_error_reporting_location(message, code):
    message.respond(u"[ERREUR] Le Lieu de rapportage %s n'existe pas."
                                                               % code)
    return True


def resp_error_death_location(message, code):
    message.respond(u"[ERREUR] Le lieu du deces %s n'existe pas."
                                                               % code)
    return True


def resp_error_dob(message):
    message.respond(u"[ERREUR] la date de naissance n'est pas valide")
    return True


def resp_error_dod(message):
    message.respond(u"[ERREUR] La date de mort n'est pas valide")
    return True


def resp_success(message, name):
    message.respond(u"[SUCCES] Le rapport de deces de %(name)s a" \
                    u" ete enregistre. " % {'name': name})
    return True


def contact_for(identity):
    return Provider.objects.get(phone_number=identity)


def parse_age_dob(age_or_dob, only_date=False):
    """ parse argument as date or age. return date and bool if estimation """

    if re.match(r'^\d{8}$', age_or_dob):
        auto = False
        parsed_date = date(int(age_or_dob[0:4]), int(age_or_dob[4:6]), \
                           int(age_or_dob[6:8]))
    else:
        auto = True
        today = date.today()
        unit = age_or_dob[-1]
        value = int(age_or_dob[:-1])
        if unit.lower() == 'y':
            parsed_date = today - timedelta(365 * value) - timedelta(160)
        elif unit.lower() == 'm':
            parsed_date = today - timedelta(30 * value) - timedelta(15)
        else:
            raise ValueError(u"Age unit unknown: %s" % unit)

    if only_date:
        return parsed_date
    else:
        return (parsed_date, auto)


def unfpa_dead_pregnant_woman(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap dpw reporting_location name dob dod death_location
                      living_children dead_children pregnant
                      pregnancy_weeks pregnancy_related_death
            exemple: 'fnuap dpw kid kadi_alou 25y 20120323 kid 2 0 0 4 1'
         Outgoing:
            [SUCCES] Le rapport de deces name a ete enregistre.
            or [ERREUR] message """

    try:
        reporting_date, reporting_location_code, name, age_or_dob, dod_text, \
        death_location_code, living_children_text, dead_children_text, \
        pregnant_text, pregnancy_weeks_text, \
        pregnancy_related_death_text = args.split()
    except:
        return resp_error(message, u"le rapport")

    # Entity code
    try:
        reporting_location = Entity.objects.get(slug=reporting_location_code)
    except Entity.DoesNotExist:
        return resp_error_reporting_location(message, reporting_location_code)

    # DOB (YYYY-MM-DD) or age (11y/11m)
    try:
        dob, dob_auto = parse_age_dob(age_or_dob)
    except:
        return resp_error_dob(message)

    # Date of Death, YYYY-MM-DD
    try:
        dod = parse_age_dob(dod_text, True)
    except:
        return resp_error_dod(message)

    # Place of death, entity code
    try:
        death_location = Entity.objects.get(slug=death_location_code)
    except Entity.DoesNotExist:
        return resp_error_death_location(message, death_location_code)

    # Nb of living children
    try:
        living_children = int(living_children_text)
    except:
        return resp_error(message, u"le nombre d'enfants vivant du defunt")

    # Nb of dead children
    try:
        dead_children = int(dead_children_text)
    except:
        return resp_error(message, u"le nombre d'enfants morts de la"
                                   u" personne decedee")

    # was she pregnant (0/1)
    pregnant = bool(int(pregnant_text))

    # Nb of weeks of pregnancy (or 0)
    try:
        pregnancy_weeks = int(pregnancy_weeks_text)
    except:
        return resp_error(message, u"la Duree de la grossesse")

    # Pregnancy related death? (0/1)
    pregnancy_related_death = bool(int(pregnancy_related_death_text))

    report = MaternalMortalityReport()
    report.created_by = contact_for(message.identity)
    report.created_on = parse_age_dob(reporting_date, True)
    report.reporting_location = reporting_location
    report.name = name.replace('_', ' ')
    report.dob = dob
    report.dob_auto = dob_auto
    report.dod = dod
    report.death_location = death_location
    report.living_children = living_children
    report.dead_children = dead_children
    report.pregnant = report.YES if pregnant else report.NO
    report.pregnancy_weeks = pregnancy_weeks
    report.pregnancy_related_death = report.YES if pregnancy_related_death \
                                                else report.NO
    report.save()

    return resp_success(message, report.name)


def unfpa_dead_children_under5(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap du5 reporting_location name dob dod death_location
         exemple: 'fnuap du5 kid alou_dolo 20111213 10121203 kid'
         Outgoing:
            [SUCCES] Le rapport de deces name a ete enregistre.
            or [ERREUR] message """

    try:
        reporting_date, reporting_location_code, name, age_or_dob, dod_text, \
        death_location_code = args.split()
    except:
        return resp_error(message, u"l'enregistrement de rapport "\
                                   u" des moins de 5ans")

    # Entity code
    try:
        reporting_location = Entity.objects.get(slug=reporting_location_code)
    except Entity.DoesNotExist:
        return resp_error_reporting_location(message, reporting_location_code)

    # DOB (YYYY-MM-DD) or age (11y/11m)
    try:
        dob, dob_auto = parse_age_dob(age_or_dob)
    except:
        return resp_error_dob(message)

    # Date of Death, YYYY-MM-DD
    try:
        dod = parse_age_dob(dod_text, True)
    except:
        return resp_error_dod(message)

    # Place of death, entity code
    try:
        death_location = Entity.objects.get(slug=death_location_code)
    except Entity.DoesNotExist:
        return resp_error_death_location(message, death_location_code)

    report = ChildrenMortalityReport()
    report.created_by = contact_for(message.identity)    
    report.created_on = parse_age_dob(reporting_date, True)
    report.reporting_location = reporting_location
    report.name = name.replace('_', ' ')
    report.dob = dob
    report.dob_auto = dob_auto
    report.dod = dod
    report.death_location = death_location

    report.save()

    return resp_success(message, report.name)
