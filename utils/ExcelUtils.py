import xlrd
from utils.StringUtils import bracketsSoup
from model.FactorFeedback import FactorFeedback
from model.SchemeFeedback import SchemeFeedback

book = xlrd.open_workbook('../resources/data.xlsx')

factorSheet = book.sheet_by_name('因素反馈')
for i in range(factorSheet.nrows):
    row = factorSheet.row_values(i)
    factor = bracketsSoup(row[0])
    res = []
    if factor != '':
        res.append([factor, row[1:]])
        FactorFeedback.resList.append(res)

schemeSheet = book.sheet_by_name('方案反馈')
scheme = ''
for i in range(schemeSheet.nrows):
    row = schemeSheet.row_values(i)
    if row[0] != '':
        scheme = row[0]
    factor = bracketsSoup(row[1])
    res = []
    if factor != '':
        res.append([scheme, factor, row[1:]])
        SchemeFeedback.resList.append(res)

for item in FactorFeedback.resList:
    print(item)

for item in SchemeFeedback.resList:
    print(item)
