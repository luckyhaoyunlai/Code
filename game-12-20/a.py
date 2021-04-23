
#结局bool 和z3bool的比较问题
from z3 import *
X=Int("X")
Y=Int("Y")
e2=And(True,True) #False
# e1=simplify(e1)
e1=True
s=Solver()
if e1==False:
    s.add(True,e2)
    if(s.check()==sat):
        print("可以打印")
if e1==True:
    s.add(True,e2)
    if(s.check()==unsat):
        print("可以打印")

# if e2 ==False:
#     s.add(And(False,e1))
#     print(s.check())
# if e2 ==True:
#     s.add(And(True,e1))
#     print(s.check())
# if(e2!=True and e2!=False):
#     e2=simplify(e2)
# print(e1)
# print(e2)
# s=Solver()
# s.add(e1)
# print(s.check())



