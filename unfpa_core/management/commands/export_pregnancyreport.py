#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import json

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy

from unfpa_core.models import PregnancyReport
from bolibana.export_utils import (get_username_from,
                                   get_entity_for,
                                   datetime_to)


def serialize_pregnancyreport(report):

    report_data = report.to_dict()

    # created_by / modified_by
    report_data.update({'created_by':
                        get_username_from(report_data.get('created_by')),
                        'modified_by':
                        get_username_from(report_data.get('modified_by'))})

    # created_on / modified_on
    report_data.update({'created_on':
                        datetime_to(report_data.get('created_on')),
                        'modified_on':
                        datetime_to(report_data.get('modified_on'))})

    # location entity
    report_data.update({'reporting_location':
                        get_entity_for(report_data.get('reporting_location'))})

    # dates
    report_data.update({'dob':
                        datetime_to(report_data.get('dob')),
                        'expected_delivery_date':
                        datetime_to(report_data.get('expected_delivery_date')),
                        'delivery_date':
                        datetime_to(report_data.get('delivery_date'))})

    # result
    report_data.update({'pregnancy_result': report.result_to_str()})

    # removed unwanted fields
    for field in ('id', ):
        if hasattr(report_data, field):
            del report_data[field]

    return report_data


class Command(BaseCommand):
    help = ugettext_lazy("Export pnlp2011 PregnancyReport to JSON")

    def handle(self, *args, **kwargs):

        data = []
        fileo = open('unfpa_maternal_death_reports.json', 'w')

        for report in PregnancyReport.objects.all():
            report_data = serialize_pregnancyreport(report)
            data.append(report_data)

            print(report)

        json.dump(data, fileo)
        fileo.close()

        print("PregnancyReport complete")
