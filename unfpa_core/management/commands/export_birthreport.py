#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import json

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy

from unfpa_core.models import BirthReport
from bolibana.export_utils import (get_username_from,
                                   get_entity_for,
                                   datetime_to)


def serialize_birth(report):

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
                        datetime_to(report_data.get('dob'))})

    # removed unwanted fields
    for field in ('id', ):
        if hasattr(report_data, field):
            del report_data[field]

    return report_data


class Command(BaseCommand):
    help = ugettext_lazy("Export pnlp2011 BirthReport to JSON")

    def handle(self, *args, **kwargs):

        data = []
        fileo = open('unfpa_birth_reports.json', 'w')

        for report in BirthReport.objects.all():
            report_data = serialize_birth(report)
            data.append(report_data)

            print(report)

        json.dump(data, fileo)
        fileo.close()

        print("BirthReport complete")
