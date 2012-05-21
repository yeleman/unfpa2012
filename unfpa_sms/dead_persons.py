#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from unfpa_core.models import MaternalMortalityReport, ChildrenMortalityReport
from bolibana.models import Entity
from common import contact_for, resp_error, resp_error_dob, resp_error_provider
from date_formate import parse_age_dob

SEX = {
    'm': ChildrenMortalityReport.MALE,
    'f': ChildrenMortalityReport.FEMALE
}

DEATHPLACE = {
    'd': ChildrenMortalityReport.HOME,
    'c': ChildrenMortalityReport.CENTER,
    'a': ChildrenMortalityReport.OTHER,
}


def resp_error_reporting_location(message, code):
    message.respond(u"[ERREUR] Le Lieu de rapportage %s n'existe pas."
                                                               % code)
    return True


def resp_error_death_location(message, code):
    message.respond(u"[ERREUR] Le lieu du deces %s n'existe pas."
                                                               % code)
    return True


def resp_error_dod(message):
    message.respond(u"[ERREUR] La date de mort n'est pas valide")
    return True


def resp_success(message, name):
    message.respond(u"[SUCCES] Le rapport de deces de %(name)s a"
                    u" ete enregistre. " % {'name': name})
    return True


def unfpa_dead_pregnant_woman(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap dpw reporting_location name dob dod death_location
                      living_children dead_children pregnant
                      pregnancy_weeks pregnancy_related_death
            exemple: 'fnuap dpw 20120430 kid blaise 20070330 20110430 kid
                      2 3 1 5 0'

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

    contact = contact_for(message.identity)

    report = MaternalMortalityReport()
    
    if contact:
        report.created_by = contact
    else:
        resp_error_provider(message)

    report.created_on = parse_age_dob(reporting_date, True)
    report.reporting_location = reporting_location
    report.name = name.replace('_', ' ')
    report.dob = dob
    report.dob_auto = dob_auto
    report.dod = dod
    report.death_location = death_location
    report.living_children = living_children
    report.dead_children = dead_children
    report.pregnant = pregnant
    report.pregnancy_weeks = pregnancy_weeks
    report.pregnancy_related_death = pregnancy_related_death
    try:
        report.save()
    except:
        return resp_error(message, u"[ERREUR] Le rapport n est pas enregiste")

    return resp_success(message, report.name)


def unfpa_dead_children_under5(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap du5 reporting_date reporting_location_code name sex
            age_or_dob dod_text death_location_code place_death
         exemple: 'fnuap du5 20120502 1488 nom F 20100502 20120502 1488 D'

         Outgoing:
            [SUCCES] Le rapport de deces name a ete enregistre.
            or [ERREUR] message """

    try:
        reporting_date, reporting_location_code, name, sex, age_or_dob, \
        dod_text, death_location_code, place_death = args.split()
    except:
        return resp_error(message, u"l'enregistrement de rapport "
                                   u" des moins de 5ans")

    # Entity code
    try:
        reporting_location = Entity.objects.get(slug=reporting_location_code)
    except Entity.DoesNotExist:
        return resp_error_reporting_location(message, reporting_location_code)

    # DOB (YYYY-MM-DD) or age (11a/11m)
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

    contact = contact_for(message.identity)

    report = ChildrenMortalityReport()

    if contact:
        report.created_by = contact
    else:
        resp_error_provider(message)

    report.created_on = parse_age_dob(reporting_date, True)
    report.reporting_location = reporting_location
    report.name = name.replace('_', ' ')
    report.sex = SEX.get(sex, ChildrenMortalityReport.MALE)
    report.dob = dob
    report.dob_auto = dob_auto
    report.dod = dod
    report.death_location = death_location
    report.death_place = DEATHPLACE.get(place_death,
                                        ChildrenMortalityReport.OTHER)
    try:
        report.save()
        resp_success(message, report.name)
    except:
        return resp_error(u"Le rapport de deces n'a pas ete enregistre.")
