import xlrd
from model.FactorRes import FactorRes


def bracketsSoup(str):
    startIndex = str.find('(') + 1
    endIndex = str.find(')')
    if endIndex == -1:
        return ''
    else:
        return str[startIndex:endIndex]


book = xlrd.open_workbook('../resources/data.xlsx')

factorSheet = book.sheet_by_name('因素反馈')
for i in range(factorSheet.nrows):
    row = factorSheet.row_values(i)
    factor = bracketsSoup(row[0])
    if factor != '':
        print(factor)
        FactorRes()
    # print(row)
    # print(row[0])
