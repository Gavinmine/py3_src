#!/usr/bin/env python3
# coding=utf-8

#　　　　　 　　┏┓ 　┏┓+ +
#　　　　　　　┏┛┻━━━┛┻┓ + +
#　　　　　　　┃　　　　　　　┃ 　
#　　　　　　　┃　　　━　　　┃ ++ + + +
# 　　 　　　  ████━████ ┃+
#　　　　　　　┃　　　　　　　┃ +
#　　　　　　　┃　　　┻　　　┃
#　　　　　　　┃　　　　　　　┃ + +
#　　　　　　　┗━┓　　　┏━┛
#　　　　　　　　┃　　　┃ + + + +
#　　　　　　　　┃　　　┃
#　　　　　　　　┃　　　┃　　　　Code is far away from bug with the animal protecting
#　　　　　　　　┃　　　┃ + 　　　　神兽保佑,代码无bug
#　　　　　　　　┃　　　┃
#　　　　　　　　┃　　　┃　　+
#　　　　　　　　┃　 　　┗━━━┓ + +
#　　　　　　　　┃ 　　　　　　　┣┓
#　　　　　　　　┃ 　　　　　　　┏┛
#　　　　　　　　┗┓┓┏━┳┓┏┛ + + + +
# 　　　　　　　　┃┫┫　┃┫┫
# 　　　　　　　　┗┻┛　┗┻┛+ + + +


from openpyxl import Workbook
from xlrd import open_workbook
from sys import exit
import re

pat=re.compile('\'(.*)\'')
alist = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']

def get_Hyperlink(sheet, match, part_name):
    is_into = 0
    for h in sheet.hyperlink_list:
        if is_into:
            if h.desc == match:
                return h
        else:
            if h.desc == part_name:
                is_into = 1

    return None


def write_execl(sheet, cindex, value, careerSheet, ignore_row = 3, cr = 1):
    nrows = sheet.nrows
    #ncols = sheet.ncols

    for r in range(nrows):
        if r < ignore_row:
            continue
        i = 0
        rvalues = sheet.row_values(r)
        if r == 3:
            for rvalue in rvalues:
                index = alist[i] + str(cr)
                careerSheet[index] = rvalue
                i += 1
            cr += 1
        else:
            mvalue = int(rvalues[cindex])
            if mvalue >= value:
                for rvalue in rvalues:
                    index = alist[i] + str(cr)
                    careerSheet[index] = rvalue
                    i += 1
                cr += 1
    return cr


if __name__ == "__main__":
    name = "CalabrioRecorded_new.xls"
    wb = open_workbook(name)
    map_sheet = wb.sheet_by_index(0)
    hyperlink = get_Hyperlink(map_sheet, 'IFP', 'DESKTOP - Daily')
    if not hyperlink:
        exit(1)

    match = pat.match(hyperlink.textmark)
    if not match:
        exit(2)

    sheet_name = match.groups()[0]
    #print(sheet_name)

    sheet = wb.sheet_by_name(sheet_name)
    mc_sheet = wb.sheet_by_index(3)

    outwb = Workbook()
    careerSheet = outwb.create_sheet('IFP')
    cr = write_execl(sheet, 11, 5, careerSheet)
    #print("cr:", cr)
    cr = write_execl(mc_sheet, 11, 5, careerSheet, 4, cr)
    #print("cr:", cr)
    outwb.save('my4.xlsx')
