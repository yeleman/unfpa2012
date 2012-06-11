#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys

from bolibana.models import Entity, EntityType


def import_locations(csv_file, use_code=False):
    """ creates Entity object off a CSV filename

    CSV FORMAT:
    NAME, CODE, TYPE CODE (N,R,D,CS,V,A,C), PARENT SLUG
    CSV file must NOT include header row. """

    f = open(csv_file)
    for line in f.readlines():
        # explode CSV line
        name, code, type_code, \
        parent_slug = line.strip().split(',')
        # convert name to unicode for django & .title()
        try:
            name = unicode(name, 'utf-8')
        except:
            pass

        # retrieve parent object if address is provided
        try:
            if use_code:
                parent = Entity.objects.get(slug=parent_slug)
            else:
                parent_id = int(parent_slug[4:])
                parent = Entity.objects.get(id=parent_id)
        except:
            parent = None
        # retrieve type from code
        if type_code == 'N':
            type = EntityType.objects.get(slug='national')
        if type_code == 'R':
            type = EntityType.objects.get(slug='region')
        if type_code == 'D':
            type = EntityType.objects.get(slug='district')
        if type_code == 'C':
            type = EntityType.objects.get(slug='cscom')
        if type_code == 'V':
            type = EntityType.objects.get(slug='village')
        if type_code == 'CS':
            type = EntityType.objects.get(slug='csref')
        if type_code == 'A':
            type = EntityType.objects.get(slug='area')

        # create and save object
        try:
            entity = Entity(name=name.title(), type=type, \
                            slug=code.lower(), parent=parent)
            entity.save()
        except:
            pass

    f.close()

if __name__ == '__main__':
    if sys.argv.__len__() < 2:
        exit(1)

    import_locations(sys.argv[1])
