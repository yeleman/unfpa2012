#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from unfpa_core.models import PregnancyReport
from bolibana.models import Entity, Provider
from dead_persons import resp_error_dob
from date_formate import parse_age_dob


def contact_for(identity):
    return Provider.objects.get(phone_number=identity)


def resp_error(message, action):
    message.respond(u"[ERREUR] Impossible de comprendre le SMS pour %s"
                                                               % action)


def unfpa_pregnancy(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap born date reporting_location householder
            father mother child dob loc sex born
        example:

           'fnuap gpw kid alou_dolo 20120509 tata_keita 45 rene_org 9 20120509
            0 20120509'
        Outgoing:
            [SUCCES] Le rapport de name a ete enregistre.
            or [ERREUR] message """

    try:
        reporting_location, householder, date_recording, name_woman, dob, \
        husband, age_pregnancy, expected_date_confinement, result, \
        date_pregnancy = args.split()
    except:
        return resp_error(message, u"le rapport")

    # Entity code
    try:
        entity = Entity.objects.get(slug=reporting_location)
    except Entity.DoesNotExist:
        return message.respond(u"Le code %s n'existe pas" % reporting_location)

    # DOB (YYYY-MM-DD) or age (11a/11m)
    dob = dob + 'a'
    try:
        dob, dob_auto = parse_age_dob(dob)
    except:
        return resp_error_dob(message)

    # date recording
    try:
        date_recording, date_recordingd = parse_age_dob(date_recording)
    except:
        return resp_error_dob(message)

    # expected date confinement
    try:
        expected, expectedd = parse_age_dob(expected_date_confinement)
    except:
        return resp_error_dob(message)

    # date pregnancy
    try:
        date_pregnancy, date_pregnancyd = parse_age_dob(date_pregnancy)
    except:
        date_pregnancy = None

    report = PregnancyReport()

    report.reporting_location = entity
    report.created_by = contact_for(message.identity)
    report.name_householder = householder.replace('_', ' ')
    report.name_woman = name_woman.replace('_', ' ')
    report.name_husband = husband.replace('_', ' ')
    report.dob = dob
    report.dob_auto = dob_auto
    report.age_pregnancy = int(age_pregnancy)
    report.date_recording = date_recording
    report.expected_date_confinement = expected
    report.date_pregnancy = date_pregnancy
    report.result_pregnancy = int(result)

    report.save()

    message.respond(u"[SUCCES] Le rapport de grossesse de %(name_woman)s "
                    u"a ete enregistre." \
                    % {'name_woman': report.name_woman})
