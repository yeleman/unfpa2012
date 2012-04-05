#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from unfpa_core.models import RHCommoditiesReport
from bolibana.models import Entity, MonthPeriod, Provider


def contact_for(identity):
    return Provider.objects.get(phone_number=identity)


def resp_error(message, action):
    message.respond(u"[ERREUR] Impossible de comprendre le SMS pour %s"
                                                               % action)

def unfpa_monthly_product_stockouts(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap mps family_planning delivery_services male_condom
            female_condom oral_pills injectable iud implants
            female_sterilization male_sterilization
            amoxicillin_ij amoxicillin_cap_gel
            amoxicillin_suspension azithromycine_tab
            azithromycine_suspension benzathine_penicillin cefexime 
            clotrimazole ergometrine_tab ergometrine_vials iron
            folate iron_folate magnesium_sulfate metronidazole
            oxytocine sources
        example: 
           'fnuap mps 2012 02 kid 1 0 1 0 0 0 0 0 0 -1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'
         Outgoing:
            [SUCCES] Le rapport de name a ete enregistre.
            or [ERREUR] message """

    try:
        args = args.replace("-", "-1")
        reporting_year, reporting_month, location_of_sdp, family_planning, \
        delivery_services, male_condom, female_condom,\
        oral_pills, injectable, iud, implants, female_sterilization, \
        male_sterilization, amoxicillin_ij, amoxicillin_cap_gel, \
        amoxicillin_suspension, azithromycine_tab, azithromycine_suspension, \
        benzathine_penicillin, cefexime, clotrimazole, ergometrine_tab, \
        ergometrine_vials, iron, folate, iron_folate, magnesium_sulfate, \
        metronidazole, oxytocine = args.split()
    except:
        return resp_error(message, u"le rapport")
    try:
        period = MonthPeriod.find_create_from(year=int(reporting_year), month=int(reporting_month))
    except:
        raise
        return message.respond(u"Cette periode (%s %s) n'existe pas" % (reporting_month, reporting_year))

    # Entity code
    try:
        entity = Entity.objects.get(slug=location_of_sdp)
    except Entity.DoesNotExist:
        return message.respond(u"Le code %s n'existe pas" % location_of_sdp)

    report = RHCommoditiesReport()

    def steril_test(val):
        if int(val) == 1:
            return report.SUPPLIES_AVAILABLE
        elif int(val) == 0:
            return report.NO
        else:
            return report.SUPPLIES_NOT_AVAILABLE

    report.type = 0
    report.period = period
    report.entity = entity
    report.created_by = contact_for(message.identity)
    report.family_planning = int(family_planning)
    report.delivery_services = int(delivery_services)
    report.male_condom = int(male_condom)
    report.female_condom = int(female_condom)
    report.oral_pills = int(oral_pills)
    report.injectable = int(injectable)
    report.iud = int(iud)
    report.implants = int(implants)
    report.female_sterilization = steril_test(female_sterilization)
    report.male_sterilization = steril_test(male_sterilization)
    report.amoxicillin_ij = int(amoxicillin_ij)
    report.amoxicillin_cap_gel = int(amoxicillin_cap_gel)
    report.amoxicillin_suspension = int(amoxicillin_suspension)
    report.azithromycine_tab = int(azithromycine_tab)
    report.azithromycine_suspension = int(azithromycine_suspension)
    report.benzathine_penicillin = int(benzathine_penicillin)
    report.cefexime = int(cefexime)
    report.clotrimazole = int(clotrimazole)
    report.ergometrine_tab = int(ergometrine_tab)
    report.ergometrine_vials = int(ergometrine_vials)
    report.iron = int(iron)
    report.folate = int(folate)
    report.iron_folate = int(iron_folate)
    report.magnesium_sulfate = int(magnesium_sulfate)
    report.metronidazole = int(metronidazole)
    report.oxytocine = int(oxytocine)
    report.save()

    message.respond(u"[SUCCES] Le rapport de %(cscom)s pour %(period)s "
                    u"a ete enregistre. " \
                    u"Le No de recu est #%(receipt)s." \
                    % {'cscom': report.entity.display_full_name(), \
                       'period': report.period, \
                       'receipt': report.receipt})