from math import ceil, floor
import sys
from model.FactorRes import FactorRes
from model.SchmeRes import SchmeRes
import numpy as np

# 以下为测试数据
A = [0,0,2,4,2,0,0,0,0,0]
B = [0,0,0,0,0,0,0,0,2,6]
C = [0,0,0,0,0,3,5,0,0,0]
D = [0,1,6,1,0,0,0,0,0,0]
A1 = [0,0,2,4,2,0,3,5,0,0]
A2 = [0,0,0,0,4,4,0,0,0,0]
B1 = [0,0,0,0,0,0,0,0,0,8]
B2 = [0,0,0,0,0,0,2,4,2,0]
B3 = [0,0,0,1,5,2,0,0,0,0]
B4 = [0,0,2,5,1,0,0,0,0,0]
B5 = [0,0,0,0,0,0,0,0,2,6]
C1 = [0,0,0,0,0,0,0,0,4,4]
C2 = [0,0,0,1,2,2,3,0,0,0]
factor_table = FactorRes(A,B,C,D,A1,A2,B1,B2,B3,B4,B5,C1,C2)

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
soil_bentonite = SchmeRes(A1,A2,B1,B2,B3,B4,B5,C1,C2,D1) # 土-膨润土

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
soil_cement = SchmeRes(A1,A2,B1,B2,B3,B4,B5,C1,C2,D1) # 土-水泥

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
msb = SchmeRes(A1,A2,B1,B2,B3,B4,B5,C1,C2,D1) # MSB

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
fmsb = SchmeRes(A1,A2,B1,B2,B3,B4,B5,C1,C2,D1) # FMSB

st_group_1 = [] # 第一组简单三角模糊判断矩阵
st_group_2 = [] # 第二组简单三角模糊判断矩阵
st_group_3 = [] # 第三组简单三角模糊判断矩阵
st_group_4 = [] # 第四组简单三角模糊判断矩阵

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
  A = [0,0,2,4,2,0,0,0,0,0]
  B = [0,0,0,0,0,0,0,0,2,6]
  C = [0,0,0,0,0,3,5,0,0,0]
  D = [0,1,6,1,0,0,0,0,0,0]
  A1 = [0,0,2,4,2,0,3,5,0,0]
  A2 = [0,0,0,0,4,4,0,0,0,0]
  B1 = [0,0,0,0,0,0,0,0,0,8]
  B2 = [0,0,0,0,0,0,2,4,2,0]
  B3 = [0,0,0,1,5,2,0,0,0,0]
  B4 = [0,0,2,5,1,0,0,0,0,0]
  B5 = [0,0,0,0,0,0,0,0,2,6]
  C1 = [0,0,0,0,0,0,0,0,4,4]
  C2 = [0,0,0,1,2,2,3,0,0,0]
  
  # 第一组计算
  temp = [1, divide(A,B),divide(A,C),divide(A,D)]
  st_group_1.append(temp)
  temp = [divide(B,A), 1,divide(B,C),divide(B,D)]
  st_group_1.append(temp)
  temp = [divide(C,A), divide(C,B),1,divide(C,D)]
  st_group_1.append(temp)
  temp = [divide(D,A), divide(D,B),divide(D,C),1]
  st_group_1.append(temp)
  
  # 第二组计算
  temp = [1, divide(A1,A2)]
  st_group_2.append(temp)
  temp = [divide(A2,A1),1]
  st_group_2.append(temp)
  
  # 第三组计算
  temp = [1, divide(B1,B2),divide(B1,B3),divide(B1,B4),divide(B1,B5)]
  st_group_3.append(temp)
  temp = [ divide(B2,B1),1,divide(B2,B3),divide(B2,B4),divide(B2,B5)]
  st_group_3.append(temp)
  temp = [divide(B3,B1),divide(B3,B1),1,divide(B3,B4),divide(B3,B5)]
  st_group_3.append(temp)
  temp = [divide(B4,B1),divide(B4,B2),divide(B4,B3),1,divide(B4,B5)]
  st_group_3.append(temp)
  temp = [divide(B5,B1),divide(B5,B2),divide(B5,B3),divide(B5,B4),1]
  st_group_3.append(temp)
  
  # 第四组计算
  temp = [1, divide(C1,C2)]
  st_group_4.append(temp)
  temp = [divide(C2,C1),1]
  st_group_4.append(temp)
  
if __name__ == '__main__':
  
  # 求三角模糊判断矩阵 并计算CR 
    get_stmatrix()
    
    print(st_group_1)
    print(st_group_3)
    eigenvalue1, featurevector1 = np.linalg.eig(np.array(st_group_1))
    eigenvalue2, featurevector2 = np.linalg.eig(np.array(st_group_3))
    
    if max((eigenvalue1)-4)/(3 * 0.89) >= 0.1 or max((eigenvalue2)-5)/(4 * 1.12) >= 0.1:
      print('CR不符合预期 需要重新收集数据...')
    
    print('ok')
    
  
    

    
  