#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from unfpa_core.models import BirthReport
from bolibana.models import Entity, Provider
from dead_persons import resp_error_dob
from date_formate import parse_age_dob
from unfpa_core.data import contact_for, resp_error


def resp_error_date(message):
    message.respond(u"[Date de visite] la date n'est pas valide.")
    return True


BIRTHPLACE = {
    'd': BirthReport.HOME,
    'c': BirthReport.CENTER,
    'a': BirthReport.OTHER
}

SEX = {
    'm': BirthReport.MALE,
    'f': BirthReport.FEMALE
}


def unfpa_birth(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap born reporting_date reporting_location family_name
            name_mother name_child dob birth_location sex born_alive
        example:
           'fnuap born 20120514 kid dolo assan mele 20120514 d m 1'
        Outgoing:
            [SUCCES] Le rapport de name a ete enregistre.
            or [ERREUR] message """

    try:
        reporting_date, reporting_location, family_name, name_mother,\
         name_child, dob, birth_location, sex, born_alive = args.split()
    except:
        resp_error(message, u"l'enregistrement de la naissance.")
        return True

    # Entity code
    try:
        entity = Entity.objects.get(slug=reporting_location)
    except Entity.DoesNotExist:
        message.respond(u"Le code %s n'existe pas." % reporting_location)
        return True

    try:
        contact = contact_for(message.identity)
    except Provider.DoesNotExist:
        message.respond(u"L'identifiant %s n'existe pas." % message.identity)
        return True

    # DOB (YYYY-MM-DD) or age (11a/11m)
    try:
        dob, dob_auto = parse_age_dob(dob)
    except:
        resp_error_dob(message)
        return True

    # Reporting date (YYYY-MM-DD)
    try:
        reporting_date, date_auto = parse_age_dob(reporting_date)
    except:
        resp_error_date(message, reporting_date)
        return True

    report = BirthReport()

    birth_location = BIRTHPLACE.get(birth_location)
    sex = SEX.get(sex)
    born_alive = bool(int(born_alive))

    # if no name of the mother
    if name_mother == '-':
        name_mother = ''

    # if no name of the child
    if name_child == '-':
        name_child = ''

    report.reporting_location = entity
    report.created_by = contact
    report.created_on = reporting_date
    report.family_name = family_name.replace('_', ' ')
    report.surname_mother = name_mother.replace('_', ' ')
    report.surname_child = name_child.replace('_', ' ')
    report.sex = sex
    report.dob = dob
    report.birth_location = birth_location
    report.dob_auto = dob_auto
    report.born_alive = born_alive

    try:
        report.save()
        message.respond(u"[SUCCES] Le rapport de naissance de" \
                        u"%(full_name_dob)s a ete enregistre." \
                        % {'full_name_dob': report.full_name_dob()})
    except:
        raise
        message.respond(u"[ERREUR] Le rapport de naissance "
                        u"\n'a pas ete enregistre.")

    return True
