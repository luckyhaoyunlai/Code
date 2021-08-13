from z3 import *

x = Int('x')

e = And(x>1,x>0,True)
S = Solver()
S.add(e)
print(S.check())

