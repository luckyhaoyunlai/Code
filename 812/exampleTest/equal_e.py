
from z3 import *
X = Int('X')
X1 = Int('X1')

#验证两个表达式等价
e1 = X!=X1+1
e2 = Or(X>X1+1,X<X1+1)
prove(e1==e2) #unsat -->生成反例

e3 =Or(X1>1,And(Not(X1>1),X>1))
print(simplify(e3))
print(Z3_simplify_get_help(main_ctx().ref()))
