#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from unfpa_core.models import BirthReport
from bolibana.models import Entity, Provider
from dead_persons import resp_error_dob
from date_formate import parse_age_dob


def contact_for(identity):
    return Provider.objects.get(phone_number=identity)

def resp_error_date(message):
    message.respond(u"[ERREUR] la date n'est pas valide")
    return True


def resp_error(message, action):
    message.respond(u"[ERREUR] Impossible de comprendre le SMS pour %s"
                                                               % action)


def unfpa_birth(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap born date reporting_location family_name
            mother child dob loc sex born
        example:
           'fnuap born 20120514 kid dolo assan mele 20120514 D M 1'
        Outgoing:
            [SUCCES] Le rapport de name a ete enregistre.
            or [ERREUR] message """

    try:
        date, reporting_location, family_name, mother, child,\
        dob, loc, sex, born = args.split()
    except:
        return resp_error(message, u"le rapport")

    # Entity code
    try:
        entity = Entity.objects.get(slug=reporting_location)
    except Entity.DoesNotExist:
        return message.respond(u"Le code %s n'existe pas" % reporting_location)

    # DOB (YYYY-MM-DD) or age (11a/11m)
    try:
        dob, dob_auto = parse_age_dob(dob)
    except:
        return resp_error_dob(message)

    try:
        reporting_date, date_auto = parse_age_dob(date)
    except:
        return resp_error_date(message)

    report = BirthReport()
    if loc == 'd':
        birth_location = report.HOME
    elif loc == 'c':
        birth_location = report.CENTER
    else:
        birth_location = report.OTHER

    if sex == 'm':
        sex = report.MAL
    else:
        sex = report.FEMALE

    if born == '1':
        born = report.YES
    else:
        born = report.NO

    if mother == '-':
        mother = ''
    if child == '-':
        mother = ''

    report.reporting_location = entity
    report.created_by = contact_for(message.identity)
    report.name_family_name = family_name.replace('_', ' ')
    report.name_mother = mother.replace('_', ' ')
    report.name_child = child.replace('_', ' ')
    report.sex = sex
    report.dob = dob
    report.birth_location = birth_location
    report.dob_auto = dob_auto
    report.born_alive = born
    report.save()

    message.respond(u"[SUCCES] Le rapport de naissance de %(name_child)s "
                    u"a ete enregistre." \
                    % {'name_child': report.name_child})
