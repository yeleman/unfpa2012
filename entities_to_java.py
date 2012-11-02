#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os

os.environ['DJANGO_SETTINGS_MODULE'] = os.environ.get('DJANGO_SETTINGS_MODULE', 
                                                      'settings')

from bolibana.models import EntityType
from unfpa_core.models import UEntity


header = """
package unfpa;

import java.util.Hashtable;

/**
 * List of static codes and names for Entities/Locations
 * Automatically generated.
 * @author reg
 */


public class StaticCodes {

    public Hashtable cercles = new Hashtable();
    public Hashtable names = new Hashtable();

    public StaticCodes() {

        // COMMUNES HASH TABLES
        // contains a list of vil_code/vil_name for each village in commune."""

cercle_intro = """
        // CERCLES HASH TABLES
        // contains a list of com_code/com_ht for each commune in cercle."""


main_intro = """
        // MAIN HASH TABLE
        // contains a list of cercle_code/cercle_ht for each cercle."""

names_intro = """
        // NAMES HASH TABLE
        // contains names of code/name for all communes and cercles"""

footer = """
    }

}"""

def println(text):
    print(text.encode('utf-8'))


println(header)

# loop on communes to add villages
for commune in UEntity.objects.filter(type__slug='commune'):

    println(u"")
    println(u"\t\t// %s" % commune.name.title())
    println(u"\t\tHashtable %s_ht = new Hashtable();" % commune.slug)

    for village in commune.get_children():

        println(u"\t\t%(com_slug)s_ht.put(\"%(vil_slug)s\", \"%(vil_name)s\");"
                % {'com_slug': commune.slug,
                   'vil_name': village.name.title(),
                   'vil_slug': village.slug})

println(cercle_intro)

for cercle in UEntity.objects.filter(type__slug='cercle'):
    println(u"")
    println(u"\t\t// %s" % cercle.name.title())
    println(u"\t\tHashtable %s_ht = new Hashtable();" % cercle.slug)

    for commune in cercle.get_children():
        println(u"\t\t%(c_slug)s_ht.put(\"%(com_slug)s\", %(com_slug)s_ht);"
                u" // %(com_name)s"
                % {'c_slug': cercle.slug,
                   'com_slug': commune.slug,
                   'com_name': commune.name.title()})

println(main_intro)

for cercle in UEntity.objects.filter(type__slug='cercle'):

    println(u"\t\tcercles.put(\"%(slug)s\", %(slug)s_ht); // %(name)s"
            % {'slug': cercle.slug, 'name': cercle.name.title()})

println(names_intro)

for entity in UEntity.objects.filter(type__slug__in=('cercle', 'commune')):
    println(u"\t\tnames.put(\"%(slug)s\", \"%(name)s\");"
            % {'slug': entity.slug, 'name': entity.name.title()})

println(footer)