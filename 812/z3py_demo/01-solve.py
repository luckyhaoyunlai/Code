# filename: 01-solve.py
"""
解方程
"""
# from pysmt import *
from z3 import *

x = Int('x')
y = Int('y')
solve(x > 2, y < 10, x + 2*y == 7)

x='213'
print(type(eval(x))==type(1)) 

