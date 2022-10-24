import xlrd
book = xlrd.open_workbook('./resource/data.xlsx')

for sheet in book.sheets():
    print(sheet.name)