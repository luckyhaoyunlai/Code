from z3 import *

X,Y,X1,Y1 = Ints('X Y X1 Y1')
con = Not(Implies(And(And(X >= 0, X1 >= 0),
                 Not(X == X1),
                 X1 >= X,
                 Not(And(X == 0, X1 == 0))),
             And(And(X1 >= X1 - X, X1 - X >= 1),
                 ForAll([Y, Y1],
                        Implies(And(And(X1 >= X1 - X,
                                        X1 - X >= 1),
                                    Y1 == X1 + -1*X1 - X,
                                    Y == X),
                                Y == Y1)))))
S=Solver()
S.add(con)
print(S.check())
m = S.model()
print(S.model())

