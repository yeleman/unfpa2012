#!/usr/bin/env python
# encoding: utf-8
# maintainer: rgaudin

import datetime
import logging
import locale
import re

from django.conf import settings

from dead_persons import unfpa_dead_pregnant_woman, unfpa_dead_children_under5
from products import (unfpa_monthly_used_products,
                      unfpa_monthly_product_stockouts)

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, settings.DEFAULT_LOCALE)


def nosms_handler(message):
    """ FNUAP SMS router """
    def main_nut_handler(message):
        keyword = 'fnuap'
        commands = {
            'dpw': unfpa_dead_pregnant_woman,
            'du5': unfpa_dead_children_under5,
            'mup': unfpa_monthly_used_products,
            'mps': unfpa_monthly_product_stockouts,
            'test': nut_test,
            'echo': nut_echo}

        if message.content.lower().startswith('fnuap '):
            for cmd_id, cmd_target in commands.items():
                command = '%s %s' % (keyword, cmd_id)
                if message.content.lower().startswith(command):
                    n, args = re.split(r'^%s\s?' \
                                       % command,
                                         message.content.lower().strip())
                    return cmd_target(message,
                                      args=args,
                                      sub_cmd=cmd_id,
                                      cmd=command)
        else:
            return False

    if main_nut_handler(message):
        message.status = message.STATUS_PROCESSED
        message.save()
        logger.info(u"[HANDLED] msg: %s" % message)
        return True
    logger.info(u"[NOT HANDLED] msg : %s" % message)
    return False


def nut_test(message, **kwargs):
    try:
        code, msg = message.content.split('fnuap test')
    except:
        msg = ''

    message.respond(u"Received on %(date)s: %(msg)s" \
                    % {'date': datetime.datetime.now(), 'msg': msg})
    return True


def nut_echo(message, **kwargs):
    message.respond(kwargs['args'])
    return True