#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.models import Provider


def contact_for(identity):
    return Provider.objects.get(phone_number=identity)


def resp_error(message, action):
    return message.respond(u"[ERREUR] Impossible de comprendre " \
                    u"le SMS pour %s" % action)
