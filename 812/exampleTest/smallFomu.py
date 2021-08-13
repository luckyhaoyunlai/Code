from z3 import *
X,X1 = Ints('X X1')

e1 = X != X1+1
e2 = X > X1+1
e3 = X < X1+1
e4 = X == X1+1

#利用z3判断e2+e3等价与e1
prove(Or(e2,e3)==e1)

#e2成立,e1一定成立
prove(Or(e1,e2)==e1)
prove(Or(e1,And(Not(e2),e3))==e1)
prove(Or(e4,e2,e3)==True)





