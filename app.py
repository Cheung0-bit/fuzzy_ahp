import sys

import numpy as np
from model.FactorFeedback import FactorFeedback
from model.SchemeFeedback import SchemeFeedback
from math import ceil
from model.Ri import Ri
from model.Fuzzy import FUZZY_TABLE

group_1 = [[0, 0, 2, 4, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 6], [0, 0, 0, 0, 0, 3, 5, 0, 0, 0],
           [0, 1, 6, 1, 0, 0, 0, 0, 0, 0]]
group_2 = [[0, 0, 0, 0, 0, 0, 3, 5, 0, 0], [0, 0, 0, 0, 4, 4, 0, 0, 0, 0], ]
group_3 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 0, 0, 0, 2, 4, 2, 0], [0, 0, 0, 1, 5, 2, 0, 0, 0, 0],
           [0, 0, 2, 5, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 6]]
group_4 = [[0, 0, 0, 0, 0, 0, 0, 0, 4, 4], [0, 0, 0, 1, 2, 2, 3, 0, 0, 0]]
group_list = [group_1, group_2, group_3, group_4]
factor_table = FactorFeedback(group_list)

A1 = [0, 0, 0, 0, 5, 3]
A2 = [0, 0, 0, 0, 6, 2]
B1 = [0, 0, 0, 0, 0, 8]
B2 = [0, 7, 1, 0, 0, 0]
B3 = [0, 0, 4, 4, 0, 0]
B4 = [0, 0, 4, 4, 0, 0]
B5 = [0, 0, 0, 0, 6, 2]
C1 = [0, 0, 0, 8, 0, 0]
C2 = [0, 0, 0, 8, 0, 0]
D1 = [0, 0, 0, 0, 4, 4]
resList = [A1, A2, B1, B2, B3, B4, B5, C1, C2, D1]
soil_bentonite = SchemeFeedback(resList)  # 土-膨润土

A1 = [0, 2, 6, 0, 0, 0]
A2 = [0, 0, 5, 3, 0, 0]
B1 = [0, 5, 3, 0, 0, 0]
B2 = [0, 0, 0, 0, 0, 8]
B3 = [0, 0, 0, 3, 5, 0]
B4 = [0, 0, 0, 2, 6, 0]
B5 = [0, 0, 0, 0, 7, 1]
C1 = [0, 0, 0, 8, 0, 0]
C2 = [0, 0, 1, 7, 0, 0]
D1 = [0, 2, 5, 1, 0, 0]
resList = [A1, A2, B1, B2, B3, B4, B5, C1, C2, D1]
soil_cement = SchemeFeedback(resList)  # 土-水泥

A1 = [0, 0, 0, 6, 2, 0]
A2 = [0, 0, 5, 3, 0, 0]
B1 = [0, 0, 0, 0, 4, 4]
B2 = [0, 0, 0, 0, 1, 7]
B3 = [0, 0, 0, 0, 2, 6]
B4 = [0, 0, 0, 0, 2, 6]
B5 = [0, 2, 5, 1, 0, 0]
C1 = [0, 0, 0, 8, 0, 0]
C2 = [0, 0, 1, 7, 0, 0]
D1 = [0, 0, 0, 8, 0, 0]
resList = [A1, A2, B1, B2, B3, B4, B5, C1, C2, D1]
msb = SchemeFeedback(resList)  # MSB

A1 = [0, 0, 5, 3, 0, 0]
A2 = [0, 0, 5, 3, 0, 0]
B1 = [0, 0, 0, 0, 4, 4]
B2 = [0, 0, 0, 0, 1, 7]
B3 = [0, 0, 0, 0, 2, 6]
B4 = [0, 0, 0, 0, 2, 6]
B5 = [0, 0, 0, 2, 5, 1]
C1 = [0, 0, 0, 8, 0, 0]
C2 = [0, 0, 1, 7, 0, 0]
D1 = [0, 0, 0, 8, 0, 0]
resList = [A1, A2, B1, B2, B3, B4, B5, C1, C2, D1]
fmsb = SchemeFeedback(resList)  # FMSB

schme_list = [soil_bentonite, soil_cement, msb, fmsb]  # 方案集合
st_group_list = []  # 简单三角模糊判断矩阵集合
pi = []  # pi分量和
sigma_sigma = [] # 双sigma求和中间值
si = [] # si 综合模糊度
relative_importance_index = []

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


# 圈乘的实现
def circle_multiplication(x, y):
    z = (x[0] * y[0], x[1] * y[1], x[2] * y[2])
    return z


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

if __name__ == '__main__':
    # 1.求三角模糊判断矩阵
    get_stmatrix()
    # 打印简单三角模糊矩阵
    print('====简单三角模糊矩阵计算完成====')
    size = len(st_group_list)
    for i in range(size):
        print('第{}组:'.format(i + 1), end=' ')
        print(st_group_list[i])

    # 2.进行简单三角模糊矩阵一致性检验 判断CR是否符合标准
    print('====开始检测CR====')
    calc_cr()

    # 3.将简单三角模糊矩阵转换为三角模糊判断矩阵
    print('====简单三角模糊矩阵--->三角模糊判断矩阵====')
    convert()
    print('处理结果:')
    size = len(st_group_list)
    for i in range(size):
        print('第{}组:'.format(i + 1), end=' ')
        print(st_group_list[i])

    # 4.计算Pi
    print('====开始计算Pi====')
    calc_pi()
    print(pi)

    # 5.获取全矩阵分量求和SIGMA AND SIGMA
    print('====开始计算全矩阵分量和====')
    calc_sigma_sigma()
    print(sigma_sigma)

    # 6.确定各分组三角模糊判断矩阵模糊综合度Si
    print('====开始计算Si====')
    calc_si()
    print(si)

    # 7.计算 Relative importance index
    print('Relative importance index')