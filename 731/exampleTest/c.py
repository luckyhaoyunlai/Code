from os import fsdecode
from z3 import *

x = Int('x')
cover = {}
term1 = 1
c = Int('c')
d = Int('d')
temp = c+c+1 == d+2+c  # c == 1 + d
temp1 = c+1 >= d+1
temp2 = c+2 > d  # Not(c <= -2 + d)
temp3 = c > d+2  # Not(c <= 2 + d)
temp4 = 1 + x > 1
temp = simplify(Not(c <= 2 + d))
print(temp)


print(simplify(c+c+1 == d+2+c))  # c == 1 + d
print(simplify(c+1 >= d+1))      # c >= d
print(simplify(c+2 > d))         # Not(c <= -2 + d)
print(simplify(1 + x < 1))     # Not(x <= 0)


# 怎样来判断一个点是否谓词

print(And(True, True))
