from z3 import *
e_num = Int('e_num')
X = Int('X')
Y = Int('Y')
e_num = Int('e_num')
specification = And(e_num >= X, e_num >= Y, Or(e_num == X, e_num == Y))

e = If(X >= Y, X, Y)

Z3exp = eval(str(specification).replace("e_num", str(e)))
s = Solver()
s.add(Not(Z3exp))
#取反 如果没有满足的+not 的结果是unsat
#如果是可能有结果的话，那么结果可能是sat
#所以说是要取反找unsat
print(s.check())
