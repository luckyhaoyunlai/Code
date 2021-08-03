from z3 import *
X,X1 = Ints('X X1')
cover = {(1, 1): [[1, 1]], (0, X): [[2, 0], [3, 1]], (0, 2): [[3, 0], [2, 0], [4, 0]], (1, X): [[2, 2], [1, 1]],
(0, X - 1): [[4, 1], [3, 0]], (1, X1): [[1, 1], [2, 2]]}

print(dict(cover[1,X])==dict(cover[1,X1]))  #True
print(cover)