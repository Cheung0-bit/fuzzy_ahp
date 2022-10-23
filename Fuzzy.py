from ctypes import sizeof


class Fuzzy:
  'TOPSIS语言变量'
  lang_var = '' # 语言变量
  stfn = '' # 简单三角模糊数
  tfn = () # 三角模糊数
  reciprocal = () # 倒数
  
  def __init__(self, lang_var, stfn, tfn, reciprocal):
    self.lang_var = lang_var
    self.stfn = stfn
    self.tfn = tfn
    self.reciprocal = reciprocal
  
  def displayFuzzy(self):
    print("语言变量: {}\t简单三角模糊数: {}\t三角模糊数: {}\t倒数: {}".format(self.lang_var,self.stfn,self.tfn,self.reciprocal))

fuzzy_table = []
fuzzy_table.append(Fuzzy('同等重要', '1', (1,1,1),(1,1,1)))
fuzzy_table.append(Fuzzy('几乎同等重要', '1`', (1,1,1),(1,1,1)))
fuzzy_table.append(Fuzzy('两者之间', '2`', (1,1,1),(1,1,1)))
fuzzy_table.append(Fuzzy('稍微重要', '3`', (1,1,1),(1,1,1)))
fuzzy_table.append(Fuzzy('两者之间', '4`', (1,1,1),(1,1,1)))
fuzzy_table.append(Fuzzy('重要', '5`', (1,1,1),(1,1,1)))
fuzzy_table.append(Fuzzy('两者之间', '6`', (1,1,1),(1,1,1)))
fuzzy_table.append(Fuzzy('很重要', '7`', (1,1,1),(1,1,1)))
fuzzy_table.append(Fuzzy('两者之间', '8`', (1,1,1),(1,1,1)))
fuzzy_table.append(Fuzzy('非常重要', '9`', (1,1,1),(1,1,1)))


for i in fuzzy_table:
  print(i.displayFuzzy())
    
  

  