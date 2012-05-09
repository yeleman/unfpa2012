#!/usr/bin/env python
# encoding: utf-8
# maintainer: fad

import re

from datetime import date, timedelta


def parse_age_dob(age_or_dob, only_date=False):
    """ parse argument as date or age. return date and bool if estimation """

    if re.match(r'^\d{8}$', age_or_dob):
        auto = False
        parsed_date = date(int(age_or_dob[0:4]), int(age_or_dob[4:6]), \
                           int(age_or_dob[6:8]))
    else:
        auto = True
        today = date.today()
        unit = age_or_dob[-1]
        value = int(age_or_dob[:-1])
        if unit.lower() == 'a':
            parsed_date = today - timedelta(365 * value) - timedelta(160)
        elif unit.lower() == 'm':
            parsed_date = today - timedelta(30 * value) - timedelta(15)
        else:
            raise ValueError(u"Age unit unknown: %s" % unit)

    if only_date:
        return parsed_date
    else:
        return (parsed_date, auto)
