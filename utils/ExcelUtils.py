import xlrd
from utils.StringUtils import bracketsSoup
from model.FactorFeedback import FactorFeedback
from model.SchemeFeedback import SchemeFeedback


def change_null_to_zero(my_list):
    return [0 if x == '' else int(x) for x in my_list]


def build_factor_and_scheme_by_excel(group_list, factor_table: FactorFeedback, schme_list):
    book = xlrd.open_workbook('./resources/data.xlsx')  # 请在resources同级目录下使用

    factor_sheet = book.sheet_by_name('因素反馈')
    res = []
    for i in range(factor_sheet.nrows):
        if i < 2:
            continue
        row = factor_sheet.row_values(i)
        factor = bracketsSoup(row[0])
        if factor != '':
            res.append(change_null_to_zero([0]+row[1:]))
        elif i != 2:  # 如果不是第一组
            group_list.append(res)
            res = []
    group_list.append(res)  # 接收最后一组
    factor_table.set_resList(group_list)

    scheme_sheet = book.sheet_by_name('方案反馈')
    res = []
    # scheme_group_list = []
    for i in range(scheme_sheet.nrows):
        if i < 2:
            continue
        row = scheme_sheet.row_values(i)
        scheme = row[0]
        if scheme != '' and i != 2:
            schme_list.append(SchemeFeedback(res))
            res = [change_null_to_zero([0]+row[2:])]
        else:
            res.append(change_null_to_zero([0]+row[2:]))
    schme_list.append(SchemeFeedback(res))

    # print("hello")


build_factor_and_scheme_by_excel([], FactorFeedback([]), [])
