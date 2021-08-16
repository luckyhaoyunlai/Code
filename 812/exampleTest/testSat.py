
from z3 import *
X,X1,X2,Y,Y1,Y2 = Ints('X X1 X2 Y Y1 Y2')
con = Not(Implies(And(And(X >= 0, X1 >= 0, X2 >= 0, X2 <= 1),And(X == X1, X < X2)),
            And(And(X1 >= 0, X2 >= 1, True, True, True),
                ForAll([Y, Y1, Y2],
                       Implies(And(And(X1 >= 0,
                                       X2 >= 1,
                                       True,
                                       True,
                                       True),
                                   And(Y1 == X1 + 0,
                                       Y2 == X2 + -1),
                                   Y == X),
                               And(Y == Y1, Y == Y2)))))
            )
                        
S = Solver()
S.add(con)
if S.check() == unsat:
    print("1111")
else:
    m = S.model()
    print(m[X].as_long(),m[X1].as_long(),m[X2].as_long())

con1 = Not(Implies(True,False))
s=Solver()
s.add(con1)
print(s.check())

con1 = Not(Implies(False,False))
s=Solver()
s.add(con1)
print(s.check())

con1 = Not(Implies(False,True))
s=Solver()
s.add(con1)
print(s.check())

con1 = Not(Implies(True,True))
s=Solver()
s.add(con1)
print(s.check())

con = Implies(And(And(X >= 1, X1 >= 0), X > X1 + 1),
            And(And(X >= X1 + 2, X1 + 2 > 1),
                ForAll([Y, Y1],
                       Implies(And(And(X >= X1 + 2,
                                       X1 + 2 > 1),
                                   And(Y == -1 + X1 + 2,
                                       If(X1 >= X1 + 2,
                                        Y1 == -1 + X1 + 2,
                                        Y1 == X1))),
                               Y == Y1 + 1))))
s = Solver()
s.add(con)
if s.check() == sat:
    m = s.model()
    print(m[X].as_long(),m[X1].as_long())
else:
    print("unsat")