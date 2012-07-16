#!/usr/bin/env python
# encoding=utf-8
# maintainer: Waraba Fad

import xlwt
import StringIO

font = xlwt.Font()
font.name = 'Verdana'
font.bold = True
font.height = 12 * 0x14

borders = xlwt.Borders()
borders.left = 1
borders.right = 1
borders.top = 1
borders.bottom = 1

center_align = xlwt.Alignment()
center_align.horz = xlwt.Alignment.HORZ_CENTER
center_align.vert = xlwt.Alignment.VERT_CENTER

left_align = xlwt.Alignment()
left_align.vert = xlwt.Alignment.HORZ_LEFT

grey44_color = xlwt.Pattern()
grey44_color.pattern = xlwt.Pattern.SOLID_PATTERN
grey44_color.pattern_fore_colour = 44

odd_color = xlwt.Pattern()
odd_color.pattern = xlwt.Pattern.SOLID_PATTERN
odd_color.pattern_fore_colour = 195

style_title = xlwt.easyxf('font: name Times New Roman, height 60, bold on')
style_title.font = font
style_title.alignment = center_align

styleheader = xlwt.easyxf('font: name Times New Roman, height 260, '
                          ' color-index white, bold on')
styleheader.borders = borders
styleheader.alignment = center_align
styleheader.pattern = grey44_color

style = xlwt.easyxf('font: name Times New Roman, bold on')
style.borders = borders
style.alignment = center_align

style_odd = xlwt.easyxf('font: name Times New Roman, bold on')
style_odd.borders = borders
style_odd.alignment = center_align
style_odd.pattern = odd_color


def add_rate(val):
    return "%s %s" % (val, "%")


def is_odd(value):
    return (value % 2) == 0


def pregnancy_as_excel(report):
    """ Export les données d'un rapport en xls """

    indicators = report

    # On crée le doc xls
    book = xlwt.Workbook(encoding='utf-8')

    # On crée une feuille nommé Report
    sheet = book.add_sheet(u"Report")

    def write_merge_p(liste, style):

        for index in liste:
            label = index.keys()[0]
            row, row1, col, col1 = index.values()[0]
            sheet.write_merge(row, row1, col, col1, label, style)

    # J'agrandi la colonne à 1.5 fois la normale.
    width_ = 0x0d00 * 1.5
    for w in range(0, 6):
        sheet.col(w).width = width_

    # Principe
    # write((nbre ligne - 1), nbre colonne, "contenu", style(optionnel).
    # write_merge((nbre ligne - 1), (nbre ligne - 1) + nbre de ligne
    # à merger, (nbre de colonne - 1), (nbre de colonne - 1) + nbre
    # de colonne à merger, u"contenu", style(optionnel)).
    row_ = 0
    sheet.write_merge(row_, row_, 0, 5,
                      u"Rapports mensuels de grossesses", style_title)
    row_ += 2
    sheet.write_merge(row_, row_, 1, 5, u"INDICATEURS", styleheader)
    sheet.write_merge(row_, row_ + 2, 0, 0, u"Mois", styleheader)
    row_ += 1
    hheader = [{"Total femmes \n enceintes": [row_, row_ + 1, 1, 1]},
               {"Accouchement \n enregistrés": [row_, row_ + 1, 2, 2]},
               {"Grossesses \n interrompues": [row_, row_ + 1, 3, 3]},
               {"Grossesses \n avec enfants vivants": [row_, row_ + 1, 4, 4]},
               {"Grossesses \n avec morts nées": [row_, row_ + 1, 5, 5]}]

    write_merge_p(hheader, style)
    n = 0
    for ind in indicators:
        month = ind["month"].full_name()
        row_ += 2
        row_rate = row_ + 1
        list_indicators = [{month: [row_, row_rate, 0, 0]},
                   {ind["fe"]: [row_, row_, 1, 1]},
                   {add_rate(ind["rate_fe"]): [row_rate, row_rate, 1, 1]},
                   {ind["ae"]: [row_, row_, 2, 2]},
                   {add_rate(ind["rate_ae"]): [row_rate, row_rate, 2, 2]},
                   {ind["gi"]: [row_, row_, 3, 3]},
                   {add_rate(ind["rate_gi"]): [row_rate, row_rate, 3, 3]},
                   {ind["av"]: [row_, row_, 4, 4]},
                   {add_rate(ind["rate_av"]): [row_rate, row_rate, 4, 4]},
                   {ind["mn"]: [row_, row_, 5, 5]},
                   {add_rate(ind["rate_mn"]): [row_rate, row_rate, 5, 5]}]

        n += 1
        if is_odd(n):
            style_ = style_odd
        else:
            style_ = style
        write_merge_p(list_indicators, style_)

    stream = StringIO.StringIO()
    book.save(stream)

    return stream


def birth_as_excel(report):
    """ Export les données d'un rapport en xls """

    indicators = report

    # On crée le doc xls
    book = xlwt.Workbook(encoding='utf-8')

    # On crée une feuille nommé Report
    sheet = book.add_sheet(u"Report")

    def write_merge_p(liste, style):

        for index in liste:
            label = index.keys()[0]
            row, row1, col, col1 = index.values()[0]
            sheet.write_merge(row, row1, col, col1, label, style)

    # J'agrandi la colonne à 1.5 fois la normale.
    width_ = 0x0d00 * 1.2
    for w in range(0, 9):
        sheet.col(w).width = width_

    # Principe
    # write((nbre ligne - 1), nbre colonne, "contenu", style(optionnel).
    # write_merge((nbre ligne - 1), (nbre ligne - 1) + nbre de ligne
    # à merger, (nbre de colonne - 1), (nbre de colonne - 1) + nbre
    # de colonne à merger, u"contenu", style(optionnel)).
    row_ = 0
    sheet.write_merge(row_, row_, 0, 8,
                      u"Rapports mensuels de naissances", style_title)
    row_ += 2
    sheet.write_merge(row_, row_, 1, 8, u"INDICATEURS", styleheader)
    sheet.write_merge(row_, row_ + 2, 0, 0, u"Mois", styleheader)
    row_ += 1
    hheader = [{u"Total naissance": [row_, row_ + 1, 1, 1]},
               {u"Domicile": [row_, row_ + 1, 2, 2]},
               {u"Centre": [row_, row_ + 1, 3, 3]},
               {u"Ailleurs": [row_, row_ + 1, 4, 4]},
               {u"Sexe masculin": [row_, row_ + 1, 5, 5]},
               {u"Sexe feminin": [row_, row_ + 1, 6, 6]},
               {u"Né vivant": [row_, row_ + 1, 7, 7]},
               {u"Mort-né": [row_, row_ + 1, 8, 8]}]

    write_merge_p(hheader, style)

    n = 0
    for ind in indicators:
        month = ind["month"].full_name()
        row_ += 2
        row_rate = row_ + 1
        list_indicators = [{month: [row_, row_rate, 0, 0]},
               {ind["birth"]: [row_, row_, 1, 1]},
               {add_rate(ind["rate_birth"]): [row_rate, row_rate, 1, 1]},
               {ind["residence"]: [row_, row_, 2, 2]},
               {add_rate(ind["rate_residence"]): [row_rate, row_rate, 2, 2]},
               {ind["center"]: [row_, row_, 3, 3]},
               {add_rate(ind["rate_center"]): [row_rate, row_rate, 3, 3]},
               {ind["other"]: [row_, row_, 4, 4]},
               {add_rate(ind["rate_other"]): [row_rate, row_rate, 4, 4]},
               {ind["male"]: [row_, row_, 5, 5]},
               {add_rate(ind["rate_male"]): [row_rate, row_rate, 5, 5]},
               {ind["female"]: [row_, row_, 6, 6]},
               {add_rate(ind["rate_female"]): [row_rate, row_rate, 6, 6]},
               {ind["alive"]: [row_, row_, 7, 7]},
               {add_rate(ind["rate_alive"]): [row_rate, row_rate, 7, 7]},
               {ind["stillborn"]: [row_, row_, 8, 8]},
               {add_rate(ind["rate_stillborn"]): [row_rate, row_rate, 8, 8]}]

        n += 1
        if is_odd(n):
            style_ = style_odd
        else:
            style_ = style
        write_merge_p(list_indicators, style_)

    stream = StringIO.StringIO()
    book.save(stream)

    return stream


def death_as_excel(report):
    """ Export les données d'un rapport en xls """

    indicators = report

    # On crée le doc xls
    book = xlwt.Workbook(encoding='utf-8')

    # On crée une feuille nommé Report
    sheet = book.add_sheet(u"Report")

    def write_merge_p(liste, style):

        for index in liste:
            label = index.keys()[0]
            row, row1, col, col1 = index.values()[0]
            sheet.write_merge(row, row1, col, col1, label, style)

    # J'agrandi la colonne à 1.5 fois la normale.
    width_ = 0x0d00 * 1.2
    for w in range(0, 7):
        sheet.col(w).width = width_

    # Principe
    # write((nbre ligne - 1), nbre colonne, "contenu", style(optionnel).
    # write_merge((nbre ligne - 1), (nbre ligne - 1) + nbre de ligne
    # à merger, (nbre de colonne - 1), (nbre de colonne - 1) + nbre
    # de colonne à merger, u"contenu", style(optionnel)).
    row_ = 0
    sheet.write_merge(row_, row_, 0, 6,
                      u"Rapports mensuels de décès infantile", style_title)
    row_ += 2
    sheet.write_merge(row_, row_, 1, 6, u"INDICATEURS", styleheader)
    sheet.write_merge(row_, row_ + 2, 0, 0, u"Mois", styleheader)
    row_ += 1
    hheader = [{u"Total décès": [row_, row_ + 1, 1, 1]},
               {u"Domicile": [row_, row_ + 1, 2, 2]},
               {u"Centre": [row_, row_ + 1, 3, 3]},
               {u"Ailleurs": [row_, row_ + 1, 4, 4]},
               {u"Sexe masculin": [row_, row_ + 1, 5, 5]},
               {u"Sexe feminin": [row_, row_ + 1, 6, 6]}]

    write_merge_p(hheader, style)

    n = 0
    for ind in indicators:
        month = ind["month"].full_name()
        row_ += 2
        row_rate = row_ + 1
        list_indicators = [{month: [row_, row_rate, 0, 0]},
                   {ind["ntd"]: [row_, row_, 1, 1]},
                   {add_rate(ind["rate_ntd"]): [row_rate, row_rate, 1, 1]},
                   {ind["dd"]: [row_, row_, 2, 2]},
                   {add_rate(ind["rate_dd"]): [row_rate, row_rate, 2, 2]},
                   {ind["dc"]: [row_, row_, 3, 3]},
                   {add_rate(ind["rate_dc"]): [row_rate, row_rate, 3, 3]},
                   {ind["da"]: [row_, row_, 4, 4]},
                   {add_rate(ind["rate_da"]): [row_rate, row_rate, 4, 4]},
                   {ind["sm"]: [row_, row_, 5, 5]},
                   {add_rate(ind["rate_sm"]): [row_rate, row_rate, 5, 5]},
                   {ind["sf"]: [row_, row_, 6, 6]},
                   {add_rate(ind["rate_sf"]): [row_rate, row_rate, 6, 6]}]

        style_ = style
        n += 1
        if is_odd(n):
            style_ = style_odd
        write_merge_p(list_indicators, style_)

    stream = StringIO.StringIO()
    book.save(stream)

    return stream
