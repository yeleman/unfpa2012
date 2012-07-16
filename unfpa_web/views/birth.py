#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou

from django.shortcuts import render
from django.http import HttpResponse

from bolibana.models import MonthPeriod
from bolibana.web.decorators import provider_permission
from unfpa_core.models import BirthReport
from unfpa_web.views.data import rate_cal
from unfpa_core import all_periods
from unfpa_core.exports import birth_as_excel


def sum_month(month):
    reports = BirthReport.periods.within(month) \
                         .filter(source=BirthReport.CREDOS)

    indicator = {'month': month, 'birth': 0, 'residence': 0, 'center': 0,
                 'other': 0, 'male': 0, 'female': 0, 'alive': 0,
                 'stillborn': 0}

    for report in reports:
        indicator['birth'] += 1
        if report.birth_location == BirthReport.HOME:
            indicator['residence'] += 1
        if report.birth_location == BirthReport.CENTER:
            indicator['center'] += 1
        if report.birth_location == BirthReport.OTHER:
            indicator['other'] += 1
        if report.sex == BirthReport.MALE:
            indicator['male'] += 1
        if report.sex == BirthReport.FEMALE:
            indicator['female'] += 1
        if report.born_alive == True:
            indicator['alive'] += 1
        if report.born_alive == False:
            indicator['stillborn'] += 1

    return indicator


@provider_permission('can_view_raw_data')
def birth(request):
    context = {'category': 'credos', 'subcategory': 'birth'}

    indicators = []
    periods = all_periods(MonthPeriod)

    evol_data = {'birth': {'label': u"Total naissance", 'values': {}},
                 'residence': {'label': u"Domicile", 'values': {}},
                 'center': {'label': u"Centre", 'values': {}},
                 'other': {'label': u"Ailleurs", 'values': {}},
                 'male': {'label': u"Sexe masculin", 'values': {}},
                 'female': {'label': u"Sexe feminin", 'values': {}},
                 'alive': {'label': u"Né vivant",
                        'values': {}},
                 'stillborn': {'label': u"Mort-né", 'values': {}}}

    for month in periods:
        indicator = sum_month(month)

        indicator['rate_birth'] = rate_cal(indicator['birth'],
                                           indicator['birth'])
        indicator['rate_residence'] = rate_cal(indicator['residence'],
                                           indicator['birth'])
        indicator['rate_center'] = rate_cal(indicator['center'],
                                           indicator['birth'])
        indicator['rate_other'] = rate_cal(indicator['other'],
                                           indicator['birth'])
        indicator['rate_male'] = rate_cal(indicator['male'],
                                           indicator['birth'])
        indicator['rate_female'] = rate_cal(indicator['female'],
                                           indicator['birth'])
        indicator['rate_alive'] = rate_cal(indicator['alive'],
                                           indicator['birth'])
        indicator['rate_stillborn'] = rate_cal(indicator['stillborn'],
                                           indicator['birth'])

        evol_data['birth']['values'][month.pid] = {'value': indicator['birth']}
        evol_data['residence']['values'][month.pid] = \
                                            {'value': indicator['residence']}
        evol_data['center']['values'][month.pid] = \
                                            {'value': indicator['center']}
        evol_data['other']['values'][month.pid] = \
                                            {'value': indicator['other']}
        evol_data['male']['values'][month.pid] = \
                                            {'value': indicator['male']}
        evol_data['female']['values'][month.pid] = \
                                            {'value': indicator['female']}
        evol_data['alive']['values'][month.pid] = \
                                            {'value': indicator['alive']}
        evol_data['stillborn']['values'][month.pid] = \
                                            {'value': indicator['stillborn']}

        indicators.append(indicator)

    context.update({'indicators': indicators,
                    'evol_data': evol_data.items(),
                    'periods': periods})

    return render(request, 'birth.html', context)


@provider_permission('can_view_indicator_data')
def excel_export(request):

    indicators = []
    periods = all_periods(MonthPeriod)
    evol_data = {'birth': {'label': u"Total naissance", 'values': {}},
                 'residence': {'label': u"Domicile", 'values': {}},
                 'center': {'label': u"Centre", 'values': {}},
                 'other': {'label': u"Ailleurs", 'values': {}},
                 'male': {'label': u"Sexe masculin", 'values': {}},
                 'female': {'label': u"Sexe feminin", 'values': {}},
                 'alive': {'label': u"Né vivant",
                        'values': {}},
                 'stillborn': {'label': u"Mort-né", 'values': {}}}
    for month in periods:
        indicator = sum_month(month)

        indicator['rate_birth'] = rate_cal(indicator['birth'],
                                           indicator['birth'])
        indicator['rate_residence'] = rate_cal(indicator['residence'],
                                           indicator['birth'])
        indicator['rate_center'] = rate_cal(indicator['center'],
                                           indicator['birth'])
        indicator['rate_other'] = rate_cal(indicator['other'],
                                           indicator['birth'])
        indicator['rate_male'] = rate_cal(indicator['male'],
                                           indicator['birth'])
        indicator['rate_female'] = rate_cal(indicator['female'],
                                           indicator['birth'])
        indicator['rate_alive'] = rate_cal(indicator['alive'],
                                           indicator['birth'])
        indicator['rate_stillborn'] = rate_cal(indicator['stillborn'],
                                           indicator['birth'])

        evol_data['birth']['values'][month.pid] = {'value': indicator['birth']}
        evol_data['residence']['values'][month.pid] = \
                                            {'value': indicator['residence']}
        evol_data['center']['values'][month.pid] = \
                                            {'value': indicator['center']}
        evol_data['other']['values'][month.pid] = \
                                            {'value': indicator['other']}
        evol_data['male']['values'][month.pid] = \
                                            {'value': indicator['male']}
        evol_data['female']['values'][month.pid] = \
                                            {'value': indicator['female']}
        evol_data['alive']['values'][month.pid] = \
                                            {'value': indicator['alive']}
        evol_data['stillborn']['values'][month.pid] = \
                                            {'value': indicator['stillborn']}
        indicators.append(indicator)

    file_name = 'Rapports mensuels de naissances.xls'

    file_content = birth_as_excel(indicators).getvalue()

    response = HttpResponse(file_content, \
                            content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    response['Content-Length'] = len(file_content)

    return response
