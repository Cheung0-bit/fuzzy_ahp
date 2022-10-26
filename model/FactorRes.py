# Deprecated
class FactorRes:
  A = [] #费用
  B = [] # 安全性
  C = [] # 应用性
  D = [] # 环境保护
  A1 = [] # 建设费用
  A2 = [] # 维护费用
  B1 = [] # 防渗性能
  B2 = [] # 强度特性
  B3 = [] # 膜效率
  B4 = [] # 扩散特性
  B5 = [] # 耐久特性
  C1 = [] # 场地特性
  C2 = [] # 气候条件
  
  def __init__(self, A, B, C, D, A1, A2, B1, B2, B3, B4, B5, C1, C2):
    self.A = A
    self.B = B
    self.C = C
    self.D = D
    self.A1 = A1
    self.A2 = A2
    self.B1 = B1
    self.B2 = B2
    self.B3 = B3
    self.B4 = B4
    self.B5 = B5
    self.C1 = C1
    self.C2 = C2
