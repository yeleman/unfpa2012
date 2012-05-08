#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from unfpa_core.models import BirthReport
from bolibana.models import Entity, Provider
from dead_persons import resp_error_dob
from date_formate import parse_age_dob


def contact_for(identity):
    return Provider.objects.get(phone_number=identity)


def resp_error(message, action):
    message.respond(u"[ERREUR] Impossible de comprendre le SMS pour %s"
                                                               % action)

def unfpa_birth(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap born date reporting_location householder
            father mother child dob loc sex born
        example: 
           'fnuap born 20120502 kid ali Adama Tata Aba 20100502 D M 1'
        Outgoing:
            [SUCCES] Le rapport de name a ete enregistre.
            or [ERREUR] message """

    try:
        date, reporting_location, householder, father, mother, child,\
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

    report.reporting_location = entity
    report.created_by = contact_for(message.identity)
    report.name_householder = householder.replace('_', ' ')
    report.name_father = father.replace('_', ' ')
    report.name_mother = mother.replace('_', ' ')
    report.name_child = child.replace('_', ' ')
    report.sex =  sex
    report.dob = dob
    report.birth_location = birth_location
    report.dob_auto = dob_auto
    report.born_alive = born
    if len(loc) != 1:
        report.other = loc
    report.save()

    message.respond(u"[SUCCES] Le rapport de %(cscom)s pour %(period)s "
                    u"a ete enregistre. " \
                    u"Le No de recu est #%(receipt)s." \
                    % {'cscom': report.reporting_location.display_full_name(), \
                       'period': report.name_householder, \
                       'receipt': report.sex})