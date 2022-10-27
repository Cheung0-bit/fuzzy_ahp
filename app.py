import functools
import sys
from math import sqrt

import numpy as np
from model.FactorFeedback import FactorFeedback
from model.Topsis import TOPSIS_TABLE
from model.Ri import Ri
from model.Fuzzy import FUZZY_TABLE
from utils.ExcelUtils import build_factor_and_scheme_by_excel

# 在init_data中初始化
group_list = []
factor_table = FactorFeedback([])  # 因素反馈
# 方案反馈表 schme_list
# soil_bentonite = SchemeFeedback([])  # 土-膨润土
# soil_cement = SchemeFeedback([])  # 土-水泥
# msb = SchemeFeedback([])  # MSB
# fmsb = SchemeFeedback([])  # FMSB
schme_list = []  # 方案集合
scheme_name_list = []  # 方案名列表

factor_count = 8  # 评价因子

st_group_list = []  # 简单三角模糊判断矩阵集合
pi = []  # pi分量和
sigma_sigma = []  # 双sigma求和中间值
si = []  # si 综合模糊度
relative_importance_index = []  # 相对重要指数
construction_cost = []  # 方案花费
rij = []  # 中间值
vij = []  # 归一化中间值 权重化的三角模糊决定矩阵
d_star = []  # d*
d_minus = []  # d-
cci = []  # cci
cci_with_name = []  # 带方案名的cci
rank = {}  # 排名


def init_data():
    build_factor_and_scheme_by_excel(group_list, factor_table, schme_list, scheme_name_list)


def print_data():
    print("====group_list====")
    for i in group_list:
        print(i)
    print("====schme_list====")
    for i in schme_list:
        print(i.resList)


def start(X):
    # 求取起始偏移量
    offset = 0
    for i in X:
        if i != 0:
            break;
        offset += 1
    return offset


def end(X):
    # 求取终止偏移量
    offset = 9
    while offset > 0:
        if X[offset] != 0:
            break;
        offset -= 1
    return offset


def get_last_max_index(array):
    target = max(array)
    res = []
    var = len(array)
    for i in range(var):
        if array[i] == target:
            res.append(i)
    return res[-1]


def divide(X, Y):
    a = get_last_max_index(X)
    b = get_last_max_index(Y)
    # 求取语言变量函数
    if a < b:
        return 1 / divide(Y, X)
    else:
        # start_up = start(X)
        # end_up = end(X)
        # start_down = start(Y)
        # end_down = end(Y)
        # lower_limit = start_up / end_down
        # upper_limit = end_up / start_down
        res = a / b
        return int(res + 0.5)


# 圈乘的实现
def circle_multiplication(x, y):
    z = (x[0] * y[0], x[1] * y[1], x[2] * y[2])
    return z


def get_max_in_all(array):
    var = []
    for i in array:
        var.append(max(i))
    return max(var)


def process_relative_importance_index():
    target = []
    for i in relative_importance_index:
        for j in i:
            target.append(j)
    return target


def show_as_group(my_list):
    size = len(my_list)
    for i in range(size):  # 根据下标可以确定数据所在的组
        print('第{}组:'.format(i + 1), end=' ')
        print(my_list[i])


def comp(x, y):
    return y[1] - x[1]


# ==========================================计算主流程============================================
def get_stmatrix():
    # 计算简单三角模糊判断矩阵
    for group in group_list:
        size = len(group)
        st_group_temp = []
        for i in range(size):
            st_group_temp_row = []
            for j in range(size):
                if i == j:
                    st_group_temp_row.append(1)
                else:
                    st_group_temp_row.append(divide(group[i], group[j]))
            st_group_temp.append(st_group_temp_row)
        st_group_list.append(st_group_temp)


# 计算CR
def calc_cr():
    i = 1
    for st_group in st_group_list:
        eigenvalue, featurevector = np.linalg.eig(np.array(st_group))
        n = len(st_group)
        ri = Ri.get(str(n))
        if ri != 0 and max((eigenvalue) - n) / ((n - 1) * ri) >= 0.1:
            print('CR不符合预期 需要重新收集数据...')
            sys.exit()
        else:
            print('第{}组CR符合标准'.format(i))
        i += 1


def convert():
    var1 = len(st_group_list)
    for i in range(var1):
        var2 = len(st_group_list[i])
        for j in range(var2):
            var3 = len(st_group_list[i][j])
            for k in range(var3):
                if j == k:
                    key = str(st_group_list[i][j][k])
                else:
                    if st_group_list[i][j][k] == 1.0:
                        st_group_list[i][j][k] = 1
                    key = str(st_group_list[i][j][k]) + '`'
                st_group_list[i][j][k] = FUZZY_TABLE.get(key)


def calc_pi():
    for st_group in st_group_list:
        array = []
        for st in st_group:
            var = len(st)
            res = [0, 0, 0]
            for i in range(var):
                res[0] += st[i][0]
                res[1] += st[i][1]
                res[2] += st[i][2]
            array.append(tuple(res))
        pi.append(array)


def calc_sigma_sigma():
    for st_group in st_group_list:
        res = [0, 0, 0]
        for st in st_group:
            var = len(st)
            for i in range(var):
                res[0] += st[i][0]
                res[1] += st[i][1]
                res[2] += st[i][2]
        sigma_sigma.append(tuple(res))


def calc_si():
    var = len(pi)
    for i in range(var):
        array = []
        _var = len(pi[i])
        for j in range(_var):
            temp = (1 / sigma_sigma[i][2], 1 / sigma_sigma[i][1], 1 / sigma_sigma[i][0])
            array.append(circle_multiplication(pi[i][j], temp))
        si.append(array)


# TODO 这里需要修改 因为并不是所有的单个都在最后一个 所以需要建立关系 这里默认按照顺序严格逻辑来处理程序
def calc_relative_im_index():
    var1 = si[0]  # 第一组
    var2 = len(var1)  # 第一组的长度
    for i in range(var2):
        var3 = []
        if i + 1 < var2:
            for index in si[i + 1]:
                var3.append(circle_multiplication(var1[i], index))
        else:
            var3.append(var1[i])
        relative_importance_index.append(var3)


def calc_construction_cost():
    for i in schme_list:
        var = []
        for index in i.resList:
            var1 = [0, 0, 0]
            var2 = len(index)
            for j in range(var2):
                if isinstance(index[j], int) and index[j] != 0:
                    var3 = TOPSIS_TABLE.get(str(j))
                    var1[0] += index[j] * var3[0]
                    var1[1] += index[j] * var3[1]
                    var1[2] += index[j] * var3[2]
            var1[0] /= factor_count
            var1[1] /= factor_count
            var1[2] /= factor_count
            var.append(tuple(var1))
        construction_cost.append(var)


def calc_rij():
    for i in construction_cost:
        var = []
        max_num = get_max_in_all(i)
        for j in i:
            var.append((j[0] / max_num, j[1] / max_num, j[2] / max_num))
        rij.append(var)


def calc_vij():
    target = process_relative_importance_index()
    for index in rij:
        var = []
        var1 = len(index)
        for i in range(var1):
            var.append(circle_multiplication(index[i], target[i]))
        vij.append(var)


def calc_double_d():
    for i in vij:
        _d_star = 0
        _d_minus = 0
        for j in i:
            _d_star += sqrt(1 / 3 * (pow(j[0] - 1, 2) + pow(j[1] - 1, 2) + pow(j[2] - 1, 2)))
            _d_minus += sqrt(1 / 3 * (pow(j[0], 2) + pow(j[1], 2) + pow(j[2], 2)))
        d_star.append(_d_star)
        d_minus.append(_d_minus)


def calc_cci():
    var = len(d_star)
    for i in range(var):
        cci.append(d_minus[i] / (d_star[i] + d_minus[i]))


def do_rank():
    count = 1
    while len(cci) != 0:
        rank['第{}名方案cc值'.format(count)] = max(cci)
        count += 1
        cci.remove(max(cci))


if __name__ == '__main__':
    # 0.初始化数据
    init_data()
    # print_data()
    # 1.求三角模糊判断矩阵
    get_stmatrix()
    # 打印简单三角模糊矩阵 🐕
    print('====简单三角模糊矩阵计算完成====')
    # size = len(st_group_list)
    # for i in range(size):  # 根据下标可以确定数据所在的组
    #     print('第{}组:'.format(i + 1), end=' ')
    #     print(st_group_list[i])
    show_as_group(st_group_list)

    # 2.进行简单三角模糊矩阵一致性检验 判断CR是否符合标准
    print('====开始检测CR====')
    calc_cr()

    # 3.将简单三角模糊矩阵转换为三角模糊判断矩阵
    print('====简单三角模糊矩阵--->三角模糊判断矩阵====')
    convert()
    print('处理结果:')
    show_as_group(st_group_list)

    # 4.计算Pi
    print('====开始计算Pi====')
    calc_pi()
    show_as_group(pi)

    # 5.获取全矩阵分量求和SIGMA AND SIGMA
    print('====开始计算全矩阵分量和====')
    calc_sigma_sigma()
    show_as_group(sigma_sigma)

    # 6.确定各分组三角模糊判断矩阵模糊综合度Si
    print('====开始计算Si====')
    calc_si()
    show_as_group(si)

    # 7.计算 Relative importance index
    print('====开始计算Relative importance index====')
    calc_relative_im_index()
    show_as_group(relative_importance_index)

    # 8.计算Construction Cost
    print('====下面开始计算Construction Cost====')
    calc_construction_cost()
    show_as_group(construction_cost)

    # 9.计算RIJ
    print('====开始计算RIJ====')
    calc_rij()
    show_as_group(rij)

    # 10.计算VIJ
    print('====开始计算VIJ====')
    calc_vij()
    show_as_group(vij)

    # 11.计算d*和d-
    print('====开始计算d*和d-====')
    calc_double_d()
    print('====d*如下：====')
    size = len(d_star)
    for i in range(size):  # 根据下标可以确定数据所在的组
        print(scheme_name_list[i] + ":", end=' ')
        print(d_star[i])
    print('====d-如下：====')
    size = len(d_minus)
    for i in range(size):  # 根据下标可以确定数据所在的组
        print(scheme_name_list[i] + ":", end=' ')
        print(d_minus[i])
    print('==== d- + d* 如下：====')
    for i in range(size):  # 根据下标可以确定数据所在的组
        print(scheme_name_list[i] + ":", end=' ')
        print(d_minus[i] + d_star[i])

    # 12.Closeness coefficient （cci）
    print('====开始计算CCI====')
    calc_cci()
    size = len(cci)
    for i in range(size):  # 根据下标可以确定数据所在的组
        print(scheme_name_list[i] + ":", end=' ')
        print(cci[i])
        cci_with_name.append([scheme_name_list[i]] + [cci[i]])

    # # 13.进行Rank
    # print('===下面开始RANK====')
    # do_rank()
    # print(rank)

    # 13.进行Rank
    print('===下面开始RANK===')
    cci_with_name.sort(key=functools.cmp_to_key(comp))
    size = len(cci_with_name)
    for i in range(size):  # 根据下标可以确定数据所在的组
        print('第{}名方案为：'.format(i + 1) + cci_with_name[i][0] + "   贴进度为：{}".format(cci_with_name[i][1]))
