from z3 import *

X,X1,k,Y,Y1 = Ints('X X1 k Y Y1')

con = Not(Implies(And(And(X >= 1, X1 >= 1),
                And(X%2 == 1, Not(X1%2 == 0)),
                X%2 == 0,
                Not(And(X == 1, X1 == 1))),
            And(And(X > 1, True),
                ForAll([Y, Y1],
                       Implies(And(And(X > 1, True),
                                   And(Y1 == 1, Y == X + -1)),
                               And(Y%2 == 1, Not(Y1%2 == 0)))))))
s = Solver()
s.add(con)
print(s.check())