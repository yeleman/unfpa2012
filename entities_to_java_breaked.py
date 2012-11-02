#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os

os.environ['DJANGO_SETTINGS_MODULE'] = os.environ.get('DJANGO_SETTINGS_MODULE', 
                                                      'settings')

# from bolibana.models import EntityType
from unfpa_core.models import UEntity


header = """
package unfpa;

import java.util.Hashtable;
"""

header2 = """

/**
 * List of static codes and names for Entities/Locations
 * Automatically generated.
 * @author reg
 */


public class StaticCodes {

    public Hashtable cercles = new Hashtable();
    public Hashtable names = new Hashtable();

    public StaticCodes() {"""


header_cercle = """
package unfpa;

import java.util.Hashtable;

/**
 * List of static codes and names for Entities/Locations
 * Automatically generated.
 * @author reg
 */

"""

function_intro = """
    public static Hashtable ht() {"""

function_outro = """
        return ht;"""

commune_intro = """
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

FILE_HANDLERS = {}

def println(text, file=None):
    text = u"%s\n" % text
    FILE_HANDLERS[file].write(text.encode('utf-8'))
    # print(text.encode('utf-8'))


def open_fh():
    # create file handlers
    FILE_HANDLERS[None] = open('StaticCodes.java', 'w+')
    for cercle in UEntity.objects.filter(type__slug='cercle'):
        FILE_HANDLERS[cercle.slug] = open('StaticCodes%(slug)s.java' 
                                          % {'slug': cercle.slug}, 'w+')


def close_fh():
    for f in FILE_HANDLERS.values():
        f.close()


# create files
open_fh()

println(header)

for cercle in UEntity.objects.filter(type__slug='cercle'):
    println(u"import unfpa.StaticCodes%(slug)s.*;" % {'slug': cercle.slug})

println(header2)

println(main_intro)

for cercle in UEntity.objects.filter(type__slug='cercle'):

    # println(u"\t\tcercles.put(\"%(slug)s\", %(slug)s_ht); // %(name)s"
    #         % {'slug': cercle.slug, 'name': cercle.name.title()})

    println(u"\t\tcercles.put(\"%(slug)s\", StaticCodes%(slug)s.ht()); // %(name)s"
            % {'slug': cercle.slug, 'name': cercle.name.title()})

println(names_intro)

for entity in UEntity.objects.filter(type__slug__in=('cercle', 'commune')):
    println(u"\t\tnames.put(\"%(slug)s\", \"%(name)s\");"
            % {'slug': entity.slug, 'name': entity.name.title()})

println(footer)

######################## cercle files

for cercle in UEntity.objects.filter(type__slug='cercle'):
    println(header_cercle, cercle.slug)

    println(u"public class StaticCodes%(slug)s {" % {'slug': cercle.slug}, cercle.slug)


    println(function_intro, cercle.slug)

    println(u"\t\tHashtable ht = new Hashtable();", cercle.slug)

    println(commune_intro, cercle.slug)
    # loop on communes to add villages
    for commune in cercle.get_children():

        println(u"", cercle.slug)
        println(u"\t\t// %s" % commune.name.title(), cercle.slug)
        println(u"\t\tHashtable %s_ht = new Hashtable();" % commune.slug, cercle.slug)

        for village in commune.get_children():

            println(u"\t\t%(com_slug)s_ht.put(\"%(vil_slug)s\", \"%(vil_name)s\");"
                    % {'com_slug': commune.slug,
                       'vil_name': village.name.title(),
                       'vil_slug': village.slug}, cercle.slug)

        println(u"\t\tht.put(\"%(com_slug)s\", %(com_slug)s_ht);"
                u" // %(com_name)s"
                % {'c_slug': cercle.slug,
                   'com_slug': commune.slug,
                   'com_name': commune.name.title()}, cercle.slug)

    println(function_outro, cercle.slug)


    # println(u"")
    # println(u"\t\t// %s" % cercle.name.title())
    # println(u"\t\tHashtable %s_ht = new Hashtable();" % cercle.slug)

    # for commune in cercle.get_children():
    #     println(u"\t\t%(c_slug)s_ht.put(\"%(com_slug)s\", %(com_slug)s_ht);"
    #             u" // %(com_name)s"
    #             % {'c_slug': cercle.slug,
    #                'com_slug': commune.slug,
    #                'com_name': commune.name.title()})

    println(footer, cercle.slug)

###################################

# close files
close_fh()
