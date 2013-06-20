#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import json

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy
import reversion

from unfpa_core.models import RHCommoditiesReport
from bolibana.export_utils import (DictDiffer,
                                   get_username_from,
                                   get_period_from,
                                   get_entity_for,
                                   datetime_to,
                                   status_to, type_to)


def get_receipt_for(report_id):
    return RHCommoditiesReport.objects.get(id=report_id).receipt


def serialize_commodities(version):

    report_data = version.field_dict

    report_data.update({'_version_date':
                        datetime_to(version.revision.date_created)})

    # status & types
    report_data.update({'_status': status_to(version.field_dict.get('_status')),
                        'type': type_to(version.field_dict.get('type'))})

    # sources
    report_data.update({'sources':
                        [get_receipt_for(s)
                        for s in version.field_dict.get('sources')]})

    # created_by / modified_by
    report_data.update({'created_by':
                        get_username_from(version.field_dict.get('created_by')),
                        'modified_by':
                        get_username_from(version.field_dict.get('modified_by'))})

    # created_on / modified_on
    report_data.update({'created_on':
                        datetime_to(version.field_dict.get('created_on')),
                        'modified_on':
                        datetime_to(version.field_dict.get('modified_on'))})

    # period
    try:
        report_data.update({'period':
                            get_period_from(version.field_dict.get('period'),
                                            version)})
    except:
        print(version.field_dict)
        raise

    # entity
    report_data.update({'entity':
                        get_entity_for(version.field_dict.get('entity'))})

    # YESNOAVAIL
    for field in ('female_sterilization', 'male_sterilization'):
        report_data.update({field:
                            RHCommoditiesReport.YESNOAVAIL_STR.get(report_data.get(field))})

    # removed unwanted fields
    for field in ('id', ):
        del report_data[field]

    return report_data


class Command(BaseCommand):
    help = ugettext_lazy("Export pnlp2011 RHCommoditiesReport to JSON")

    def handle(self, *args, **kwargs):

        data = []
        fileo = open('unfpa_commodities_reports.json', 'w')

        # Export MalariaReport
        for report in RHCommoditiesReport.objects.all():
            # reversions
            report_data = None
            version_list = reversion.get_unique_for_object(report)
            # Reports might not have any revision
            if not version_list:
                with reversion.create_revision():
                    report.save()
                    reversion.set_user(report.created_by.user)
                version_list = reversion.get_unique_for_object(report)
            updates = []
            for version in reversed(version_list):
                if report_data is None:
                    report_data = serialize_commodities(version)
                else:
                    new_version = serialize_commodities(version)
                    diff = DictDiffer(new_version, report_data)
                    version_update = {}
                    for field in diff.changed():
                        version_update.update({field: new_version.get(field)})
                    updates.append(version_update)

            report_data.update({'updates': updates})

            data.append(report_data)
            print(report)

        json.dump(data, fileo)
        fileo.close()

        print("RHCommoditiesReport complete")
