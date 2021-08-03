# filename: 21-bit_move.py
"""
位运算，左移、右移
"""
from z3 import *

# 创建32位x,y
x, y = BitVecs('x y', 32)

solve(x >> 2 == 3)
solve(x << 2 == 3)
solve(x << 2 == 24)

print(4>>2)
print(19>>2)
print(9<<2)
#<<在后面添加两个0
#>>消去前面两个数
