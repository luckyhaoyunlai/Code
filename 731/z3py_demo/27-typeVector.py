# filename: 27-typeVector.py
"""
εε»Ίει
"""
from z3 import *

X = IntVector('x', 5)
Y = RealVector('y', 5)
P = BoolVector('p', 5)
print(X)
print(Y)
print(P)
print([ y**2 for y in Y ])
print(Sum([ y**2 for y in Y ]))
