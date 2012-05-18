#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.models import Provider


def contact_for(identity):
    try:
        provider = Provider.objects.get(phone_number=identity)
    except Provider.DoesNotExist:
        provider = None

    return provider


def resp_error(message, action):
    message.respond(u"[ERREUR] Impossible de comprendre " \
                    u"le SMS pour %s" % action)
    return True

def conv_str_int(value):
    try:
        value = int(value)
    except:
        value = None
    return value

