from operator import gt
from z3 import *
# x = Int('x')
# y = Int('y')
# z = Bool('z')


# def Z3_ite(c, a, b):
#     return


# z = x >= y
# s = Solver()
# s.add(And(Z3_ite(z, x, y) >= x, Z3_ite(z, x, y) >= y),
#       Or((Z3_ite(z, x, y) == y), (Z3_ite(z, x, y) == x)))


# F, H, A, B, C = Bools('F H A B C')
# B, C = Ints('B,C')
B = Int('B')
C = Int('C')

s = Solver()
#If（C,T,T）-->T 
s.add(And(If(B+C<=2), 1, 0 >= B, If(gt(B, C), B, C) >= C,
          Or(If(gt(B, C), B, C) == B, If(gt(B, C), B, C) == C)))

print(s.check())
