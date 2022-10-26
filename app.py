from math import ceil, floor
from model.FactorFeedback import FactorFeedback
import numpy as np

from model.SchemeFeedback import SchemeFeedback

group_1 = [[0,0,2,4,2,0,0,0,0,0],[0,0,0,0,0,0,0,0,2,6],[0,0,0,0,0,3,5,0,0,0],[0,1,6,1,0,0,0,0,0,0]]
group_2 = [[0,0,2,4,2,0,3,5,0,0],[0,0,0,0,4,4,0,0,0,0],]
group_3 = [[0,0,0,0,0,0,0,0,0,8],[0,0,0,0,0,0,2,4,2,0],[0,0,0,1,5,2,0,0,0,0],[0,0,2,5,1,0,0,0,0,0],[0,0,0,0,0,0,0,0,2,6]]
group_4 = [[0,0,0,0,0,0,0,0,4,4],[0,0,0,1,2,2,3,0,0,0]]
group_list = [group_1,group_2,group_3,group_4]
factor_table = FactorFeedback(group_list)

A1 = [0,0,0,0,5,3]
A2 = [0,0,0,0,6,2]
B1 = [0,0,0,0,0,8]
B2 = [0,7,1,0,0,0]
B3 = [0,0,4,4,0,0]
B4 = [0,0,4,4,0,0]
B5 = [0,0,0,0,6,2]
C1 = [0,0,0,8,0,0]
C2 = [0,0,0,8,0,0]
D1 = [0,0,0,0,4,4]
resList = [A1,A2,B1,B2,B3,B4,B5,C1,C2,D1]
soil_bentonite = SchemeFeedback(resList) # 土-膨润土

A1 = [0,2,6,0,0,0]
A2 = [0,0,5,3,0,0]
B1 = [0,5,3,0,0,0]
B2 = [0,0,0,0,0,8]
B3 = [0,0,0,3,5,0]
B4 = [0,0,0,2,6,0]
B5 = [0,0,0,0,7,1]
C1 = [0,0,0,8,0,0]
C2 = [0,0,1,7,0,0]
D1 = [0,2,5,1,0,0]
resList = [A1,A2,B1,B2,B3,B4,B5,C1,C2,D1]
soil_cement = SchemeFeedback(resList) # 土-水泥

A1 = [0,0,0,6,2,0]
A2 = [0,0,5,3,0,0]
B1 = [0,0,0,0,4,4]
B2 = [0,0,0,0,1,7]
B3 = [0,0,0,0,2,6]
B4 = [0,0,0,0,2,6]
B5 = [0,2,5,1,0,0]
C1 = [0,0,0,8,0,0]
C2 = [0,0,1,7,0,0]
D1 = [0,0,0,8,0,0]
resList = [A1,A2,B1,B2,B3,B4,B5,C1,C2,D1]
msb = SchemeFeedback(resList) # MSB

A1 = [0,0,5,3,0,0]
A2 = [0,0,5,3,0,0]
B1 = [0,0,0,0,4,4]
B2 = [0,0,0,0,1,7]
B3 = [0,0,0,0,2,6]
B4 = [0,0,0,0,2,6]
B5 = [0,0,0,2,5,1]
C1 = [0,0,0,8,0,0]
C2 = [0,0,1,7,0,0]
D1 = [0,0,0,8,0,0]
resList = [A1,A2,B1,B2,B3,B4,B5,C1,C2,D1]
fmsb = SchemeFeedback(resList) # FMSB

schme_list = [soil_bentonite, soil_cement, msb, fmsb] # 方案集合

st_group_list = [] # 简单三角模糊判断矩阵集合


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
  
def divide(X,Y):
  # 求取语言变量函数
  if end(X) <= start(Y):
    return 1 / divide(Y,X)
  else:
    start_up = start(X)
    end_up = end(X)
    start_down = start(Y)
    end_down = end(Y)
    lower_limit = start_up / end_down
    upper_limit = end_up / start_down
    res = X.index(max(X)) / Y.index(max(Y))
    if res >= lower_limit and res <= upper_limit:
      res = ceil(res)
    else:
      res = floor(res)
    return res
  
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
          st_group_temp_row.append(divide(group[i],group[j]))
      st_group_temp.append(st_group_temp_row)
    st_group_list.append(st_group_temp)

# 计算CR
def calc_cr():
  for st_group in st_group_list:
    eigenvalue, featurevector = np.linalg.eig(np.array(st_group))
    n = len(st_group)
    RI = 0
    
    if max((eigenvalue)-4)/(3 * RI) >= 0.1 or max((eigenvalue2)-5)/(4 * 1.12) >= 0.1:
      print('CR不符合预期 需要重新收集数据...')

if __name__ == '__main__':
  
  # 1.求三角模糊判断矩阵
  get_stmatrix()
  print(st_group_list) # 打印简单三角模糊矩阵

  # 2.进行判断矩阵一致性检验 判断CR是否符合标准
  calc_cr()


    

    
    # print('ok')
    
  
    

    
  