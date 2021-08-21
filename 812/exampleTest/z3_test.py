from z3 import *
from operator import gt
B = Int('B')
C = Int('C')

s = Solver()
sat = "If(gt(B, C), B, C) >= B, If(gt(B, C), B, C) >= C, Or(If(gt(B, C), B, C) == B, If(gt(B, C), B, C) == C)"

pts = [{'input': [1, 2], 'output':3}]
print([1, 2] in pts['inout'])
s.add(And(eval(sat)))

a = And()

print(s.check())
