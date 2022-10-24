import xlrd
book = xlrd.open_workbook('../resources/data.xlsx')

for sheet in book.sheets():
    print(sheet.name)