#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from datetime import datetime

from unfpa_core.models import EpidemiologyReport
from bolibana.models import Entity, WeekPeriod
from unfpa_sms.common import (contact_for, resp_error, resp_error_dob,
                             resp_error_provider, parse_age_dob,
                             resp_error_date)


def unfpa_epidemiology(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap profile year number_week code_reporting_location

        example:
           'fnuap epid e 2012 1 v01619 1 1 2 2 3 3 4 4 5 5 6 6 7 7 8 8 9 9 10 10 11 11'

        Outgoing:
            [SUCCES] Le rapport de name a ete enregistre.
            or [ERREUR] message """

    try:
        profile, reporting_year, reporting_week, reporting_location, \
        acute_flaccid_paralysis_case, acute_flaccid_paralysis_death, \
        influenza_a_h1n1_case, influenza_a_h1n1_death, cholera_case, \
        cholera_death, red_diarrhea_case, red_diarrhea_death, measles_case, \
        measles_death, yellow_fever_case, yellow_fever_death, \
        neonatal_tetanus_case, neonatal_tetanus_death, meningitis_case, \
        meningitis_death, rabies_case, rabies_death, \
        acute_measles_diarrhea_case, acute_measles_diarrhea_death, \
        other_notifiable_disease_case, \
        other_notifiable_disease_death = args.split()
    except:
        return resp_error(message, u"l'enregistrement de la naissance.")

    # Entity code
    try:
        entity = Entity.objects.get(slug=reporting_location)
    except Entity.DoesNotExist:
        message.respond(u"Le code %s n'existe pas." % reporting_location)
        return True

    try:
        print reporting_year, reporting_week
        period = WeekPeriod.find_create_by_weeknum(int(reporting_year),
                                    int(reporting_week))
    except:
        message.respond(u"La periode (%s %s) n'est pas valide" %
                        (reporting_week, reporting_year))
        return True

    report = EpidemiologyReport()
    report.type = 0
    report.period = period

    report.entity = entity
    report.acute_flaccid_paralysis_case = acute_flaccid_paralysis_case
    report.acute_flaccid_paralysis_death = acute_flaccid_paralysis_death
    report.influenza_a_h1n1_case = influenza_a_h1n1_case
    report.influenza_a_h1n1_death = influenza_a_h1n1_death
    report.cholera_case = cholera_case
    report.cholera_death = cholera_death
    report.red_diarrhea_case = red_diarrhea_case
    report.red_diarrhea_death = red_diarrhea_death
    report.measles_case = measles_case
    report.measles_death = measles_death
    report.yellow_fever_case = yellow_fever_case
    report.yellow_fever_death = yellow_fever_death
    report.neonatal_tetanus_case = neonatal_tetanus_case
    report.neonatal_tetanus_death = neonatal_tetanus_death
    report.meningitis_case = meningitis_case
    report.meningitis_death = meningitis_death
    report.rabies_case = rabies_case
    report.rabies_death = rabies_death
    report.acute_measles_diarrhea_case = acute_measles_diarrhea_case
    report.acute_measles_diarrhea_death = acute_measles_diarrhea_death
    report.other_notifiable_disease_case = other_notifiable_disease_case
    report.other_notifiable_disease_death = other_notifiable_disease_death

    contact = contact_for(message.identity)

    if contact:
        report.created_by = contact
    else:
        return resp_error_provider(message)

    try:
        report.save()
        report.created_on = datetime.today()
        report.save()
        message.respond(u"[SUCCES] Le rapport de naissance de" \
                        u"%(full_name_dob)s a ete enregistre." \
                        % {'full_name_dob': report.full_name_dob()})
    except:
        raise
        message.respond(u"[ERREUR] Le rapport de naissance "
                        u"n'a pas ete enregistre.")

    return True
