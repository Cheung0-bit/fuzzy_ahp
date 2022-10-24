class Topsis:
  lang_var = '' # 语言变量
  tfn = () # 三角模糊数
  
  def __init__(self, lang_var, tfn):
    self.lang_var = lang_var
    self.tfn = tfn
  
TOPSIS_TABLE = []
TOPSIS_TABLE.append(Topsis('非常差',(1,2,3)))
TOPSIS_TABLE.append(Topsis('差',(2,3,4)))
TOPSIS_TABLE.append(Topsis('一般',(3,4,5)))
TOPSIS_TABLE.append(Topsis('好',(4,5,6)))
TOPSIS_TABLE.append(Topsis('非常好',(5,7,9)))