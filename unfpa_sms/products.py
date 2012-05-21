#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from unfpa_core.models import RHCommoditiesReport
from bolibana.models import Entity, MonthPeriod
from common import contact_for, resp_error, resp_error_provider


YESNOAVAIL = {
    '0': RHCommoditiesReport.NO,
    '1': RHCommoditiesReport.SUPPLIES_AVAILABLE,
    '2': RHCommoditiesReport.SUPPLIES_NOT_AVAILABLE,
}


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
           'fnuap mps 2012 02 1488 1 0 1 0 0 0 0 0 0 -1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'
         Outgoing:
            [SUCCES] Le rapport de name a ete enregistre.
            or [ERREUR] message """

    try:
        # -1 represente le non disponible
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
        resp_error(message, u"le rapport")
        return True

    try:
        period = MonthPeriod.find_create_from(year=int(reporting_year), month=int(reporting_month))
    except:
        message.respond(u"La periode (%s %s) n'est pas valide" % (reporting_month, reporting_year))
        return True

    # Entity code
    try:
        entity = Entity.objects.get(slug=location_of_sdp)
    except Entity.DoesNotExist:
        message.respond(u"Le code %s n'existe pas" % location_of_sdp)
        return True

    def check_int(val):
        try:
            return int(val)
        except:
            return -1

    contact = contact_for(message.identity)

    report = RHCommoditiesReport()
    if contact:
        report.created_by = contact
    else:
        resp_error_provider(message)
        return True

    report.type = 0
    report.period = period
    report.entity = entity
    report.family_planning = check_int(family_planning)
    report.delivery_services = check_int(delivery_services)
    report.male_condom = check_int(male_condom)
    report.female_condom = check_int(female_condom)
    report.oral_pills = check_int(oral_pills)
    report.injectable = check_int(injectable)
    report.iud = check_int(iud)
    report.implants = check_int(implants)
    report.female_sterilization = YESNOAVAIL.get(female_sterilization, RHCommoditiesReport.NO)
    report.male_sterilization = YESNOAVAIL.get(male_sterilization, RHCommoditiesReport.NO)
    report.amoxicillin_ij = check_int(amoxicillin_ij)
    report.amoxicillin_cap_gel = check_int(amoxicillin_cap_gel)
    report.amoxicillin_suspension = check_int(amoxicillin_suspension)
    report.azithromycine_tab = check_int(azithromycine_tab)
    report.azithromycine_suspension = check_int(azithromycine_suspension)
    report.benzathine_penicillin = check_int(benzathine_penicillin)
    report.cefexime = check_int(cefexime)
    report.clotrimazole = check_int(clotrimazole)
    report.ergometrine_tab = check_int(ergometrine_tab)
    report.ergometrine_vials = check_int(ergometrine_vials)
    report.iron = check_int(iron)
    report.folate = check_int(folate)
    report.iron_folate = check_int(iron_folate)
    report.magnesium_sulfate = check_int(magnesium_sulfate)
    report.metronidazole = check_int(metronidazole)
    report.oxytocine = check_int(oxytocine)

    try:
        report.save()
    except:
        message.respond(message, u"[ERREUR] Le rapport n est pas enregiste")
        return True

    message.respond(u"[SUCCES] Le rapport de %(cscom)s pour %(period)s "
                    u"a ete enregistre. " \
                    u"Le No de recu est #%(receipt)s." \
                    % {'cscom': report.entity.display_full_name(), \
                       'period': report.period, \
                       'receipt': report.receipt})
    return True