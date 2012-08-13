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


def children_as_excel(report, period):
    """ Export les données d'un rapport en xls """

    # On crée le doc xls
    book = xlwt.Workbook(encoding='utf-8')
    period_type = period.type()

    if period_type == "week":
        type_ = u"HEBDOMADAIRE"
    if period_type == "month":
        type_ = u"MENSUEL"
    if period_type == "quarter":
        type_ = u"TRIMESTRIEL"
    else:
        type_ = u"ANNUEL"

    # On crée une feuille nommé Report
    sheet = book.add_sheet(u"Mortalite infantiles")

    sheet.col(0).width = 0x0d00 * 3

    def write_merge_p(liste, style):

        for index in liste:
            label = index.keys()[0]
            row, row1, col, col1 = index.values()[0]
            sheet.write_merge(row, row1, col, col1, label, style)

    row_ = 0
    title = u"RAPPORT %s DU %s AU %s" % (type_,
                                        period.start_on.strftime(u"%x"),
                                        period.end_on.strftime(u"%x"))

    sheet.write_merge(0, 0, 0, 2, unicode(title), style)
    row_ += 3

    if period.type() == "week" or period.type() == "month":
        sheet.col(1).width = 0x0d00 * 3
        hheader = [{u"DISTRICT": [row_, row_ + 1, 0, 0]},
                   {u"NOMBRE DE DÉCÈS INFANTILES": [row_, row_ + 1, 1, 1]}]

        write_merge_p(hheader, styleheader)
        row_ += 1
        for disdata in report:
            row_ += 1
            sheet.write(row_, 0, "%s" % (disdata["district"]), style)
            sheet.write(row_, 1, int(disdata["deaths"]), style)

    if period.type() == "quarter" or period.type() == "year":
        col = 0
        for month in period.months:
            col += 1
            sheet.write(row_, col, "%s" % (month), styleheader)

        hheader = [{u"DISTRICT": [row_, row_, 0, 0]},
                   {u"Total": [row_, row_, col + 1, col + 1]},
                   {u"%": [row_, row_, col + 2, col + 2]}]

        write_merge_p(hheader, styleheader)
        row_ += 1

        for disdata in report:
            col = 0
            sheet.write(row_, col, "%s" % (disdata["district"]), style)
            for mdeath in disdata["mdeaths"]:
                col += 1
                sheet.write(row_, col, int(mdeath), style)

            sheet.write(row_, col + 1, "%s" % (disdata["total"]), style)
            sheet.write(row_, col + 2, "%s" % (disdata["percent_of_all"]),
                                                                   style)
            row_ += 1

    stream = StringIO.StringIO()
    book.save(stream)

    return stream


def maternal_as_excel(report, period):
    """ Export les données d'un rapport en xls """

    # On crée le doc xls
    book = xlwt.Workbook(encoding='utf-8')
    period_type = period.type()

    if period_type == "week":
        type_ = u"HEBDOMADAIRE"
    if period_type == "month":
        type_ = u"MENSUEL"
    if period_type == "quarter":
        type_ = u"TRIMESTRIEL"
    else:
        type_ = u"ANNUEL"

    # On crée une feuille nommé Report
    sheet = book.add_sheet(u"Mortalite maternelle")

    sheet.col(0).width = 0x0d00 * 3

    def write_merge_p(liste, style):

        for index in liste:
            label = index.keys()[0]
            row, row1, col, col1 = index.values()[0]
            sheet.write_merge(row, row1, col, col1, label, style)

    row_ = 0
    title = u"RAPPORT %s DU %s AU %s" % (type_,
                                        period.start_on.strftime(u"%x"),
                                        period.end_on.strftime(u"%x"))

    sheet.write_merge(0, 0, 0, 2, unicode(title), style)
    row_ += 3

    if period.type() == "week" or period.type() == "month":

        sheet.col(1).width = 0x0d00 * 3
        hheader = [{u"DISTRICT": [row_, row_ + 1, 0, 0]},
                   {u"NOMBRE DE DÉCÈS INFANTILES": [row_, row_ + 1, 1, 1]}]

        write_merge_p(hheader, styleheader)
        row_ += 1
        for disdata in report:
            row_ += 1
            sheet.write(row_, 0, "%s" % (disdata["district"]), style)
            sheet.write(row_, 1, int(disdata["deaths"]), style)

    if period.type() == "quarter" or period.type() == "year":
        col = 0
        for month in period.months:
            col += 1
            sheet.write(row_, col, "%s" % (month), styleheader)

        hheader = [{u"DISTRICT": [row_, row_, 0, 0]},
                   {u"Total": [row_, row_, col + 1, col + 1]},
                   {u"%": [row_, row_, col + 2, col + 2]}]

        write_merge_p(hheader, styleheader)
        row_ += 1

        for disdata in report:
            col = 0
            sheet.write(row_, col, "%s" % (disdata["district"]), style)
            for mdeath in disdata["mdeaths"]:
                col += 1
                sheet.write(row_, col, int(mdeath), style)

            sheet.write(row_, col + 1, "%s" % (disdata["total"]), style)
            sheet.write(row_, col + 2, "%s" % (disdata["percent_of_all"]),
                                                                   style)
            row_ += 1

    stream = StringIO.StringIO()
    book.save(stream)

    return stream


def commodities_as_excel(report, period):
    """ Export les données d'un rapport en xls """

    # On crée le doc xls
    book = xlwt.Workbook(encoding='utf-8')
    period_type = period.type()

    if period_type == "month":
        type_ = u"MENSUEL"
    elif period_type == "quarter":
        type_ = u"TRIMESTRIEL"
    else:
        type_ = u"ANNUEL"


    # On crée une feuille nommé Report
    sheet = book.add_sheet(u"Produits dispo")

    sheet.col(0).width = 0x0d00 * 4
    sheet.col(1).width = 0x0d00 * 3

    def write_merge_p(liste, style):

        for index in liste:
            label = index.keys()[0]
            row, row1, col, col1 = index.values()[0]
            sheet.write_merge(row, row1, col, col1, label, style)


    if period.type() == "month":
        row_ = 0
        title = u"RAPPORT %s DU %s AU %s" % (type_,
                                        period.start_on.strftime(u"%x"),
                                        period.end_on.strftime(u"%x"))

        sheet.write_merge(0, 0, 0, 2, unicode(title), style)
        row_ += 3

        hheader = [{u"INDICATEURS": [row_, row_ + 1, 0, 0]},
                   {u"NOMBRE DE CENTRES": [row_, row_ + 1, 1, 1]}]

        write_merge_p(hheader, styleheader)
        row_ += 1

        fp_services = report["fp_services"]
        delivery_services = report["delivery_services"]
        both_services = report["both_services"]
        fp_stockout = report["fp_stockout"]
        atleast_3methods = report["atleast_3methods"]
        # atleast_3methods_percent = report["atleast_3methods_percent"]
        otoxycin_magnesium_stockout = report["otoxycin_magnesium_stockout"]

        row_ += 1

        sheet.write(row_, 0, "Centres proposant le planning familial" , style)
        sheet.write(row_, 1, "%s" % (fp_services[0]) , style)
        row_ += 1

        sheet.write(row_, 0, "Centres pratiquant les accouchements" , style)
        sheet.write(row_, 1, "%s" % (delivery_services[0]) , style)
        row_ += 1

        sheet.write(row_, 0, "Centres proposant le P.F et les accouchements" , style)
        sheet.write(row_, 1, "%s" % (both_services[0]) , style)
        row_ += 1

        sheet.write(row_, 0, "Centres en rupture de méthodes de PF indiv." , style)
        sheet.write(row_, 1, "%s" % (fp_stockout[0]) , style)
        row_ += 1

        sheet.write(row_, 0, "Centres offrants au moins 3 méthodes de P.F" , style)
        sheet.write(row_, 1, "%s" % (atleast_3methods[0]) , style)
        row_ += 1

        sheet.write(row_, 0, "Centres en rupture d'Oxytocine et de sulphate de magnésium" , style)
        sheet.write(row_, 1, "%s" % (otoxycin_magnesium_stockout[0]) , style)

        row_ += 3
        title1 = u"Centre en ruptures de stock de méthodes de planification familiale"
        sheet.write(row_, 0, unicode(title1), style)
        row_ += 1
        hheader = [{u"Centre": [row_, row_ + 1, 0, 0]},
                   {u"P.M.": [row_, row_ + 1, 1, 1]},
                   {u"P.F.": [row_, row_ + 1, 2, 2]},
                   {u"C.O.": [row_, row_ + 1, 3, 3]},
                   {u"IJ": [row_, row_ + 1, 4, 4]},
                   {u"D.I.U.": [row_, row_ + 1, 5, 5]},
                   {u"Implants": [row_, row_ + 1, 6, 6]},
                   {u"S.F.": [row_, row_ + 1, 7, 7]},
                   {u"S.M.": [row_, row_ + 1, 8, 8]}]

        write_merge_p(hheader, styleheader)
        row_ += 2
        for disdata in report['all_stock_outs']:


            sheet.write(row_, 0, '%s/%s' % (disdata['district'].name,
                                            disdata['nb_centers']),
                        style)
            sheet.write(row_, 1,
                        u'%s/%s' % (disdata['stock_outs']['male_condom'][0],
                        str(disdata['stock_outs']['male_condom'][1]) + '%'),
                        style)
            sheet.write(row_, 2,
                        u'%s/%s' % (disdata['stock_outs']['female_condom'][0],
                        str(disdata['stock_outs']['female_condom'][1]) + '%'),
                        style)
            sheet.write(row_, 3,
                        u'%s/%s' % (disdata['stock_outs']['oral_pills'][0],
                        str(disdata['stock_outs']['oral_pills'][1]) + '%'),
                        style)
            sheet.write(row_, 4,
                        u'%s/%s' % (disdata['stock_outs']['injectable'][0],
                        str(disdata['stock_outs']['injectable'][1]) + '%'),
                        style)
            sheet.write(row_, 5,
                        u'%s/%s' % (disdata['stock_outs']['iud'][0],
                        str(disdata['stock_outs']['iud'][1]) + '%'), style)
            sheet.write(row_, 6,
                        u'%s/%s' % (disdata['stock_outs']['implants'][0],
                        str(disdata['stock_outs']['implants'][1]) + '%'),
                        style)
            sheet.write(row_, 7,
                u'%s/%s' % (disdata['stock_outs']['female_sterilization'][0],
                str(disdata['stock_outs']['female_sterilization'][1]) + '%'),
                style)
            sheet.write(row_, 8,
                u'%s/%s' % (disdata['stock_outs']['male_sterilization'][0],
                str(disdata['stock_outs']['male_sterilization'][1]) + '%'),
                style)
            row_ += 1

    if period.type() == "quarter" or period.type() == "year":
        col = 0
        for month in period.months:
            col += 1
            sheet.write(row_, col, "%s" % (month), styleheader)

        hheader = [{u"DISTRICT": [row_, row_, 0, 0]},
                   {u"Total": [row_, row_, col + 1, col + 1]},
                   {u"%": [row_, row_, col + 2, col + 2]}]

        write_merge_p(hheader, styleheader)
        row_ += 1

        for disdata in report:
            col = 0
            sheet.write(row_, col, "%s" % (disdata["district"]), style)
            for mdeath in disdata["mdeaths"]:
                col += 1
                sheet.write(row_, col, int(mdeath), style)

            sheet.write(row_, col + 1, "%s" % (disdata["total"]), style)
            sheet.write(row_, col + 2, "%s" % (disdata["percent_of_all"]),
                                                                   style)
            row_ += 1

    stream = StringIO.StringIO()
    book.save(stream)

    return stream
