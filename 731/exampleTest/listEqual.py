# dictionary update sequence element #0 has length 1; 2 is required
from typing import Counter
import copy

from z3.z3printer import print_matrix


list1 = [[1], [2]]
list2 = [[2], [1]]
list3 = [[1, 2], [3, 4]]
list4 = [[3, 4], [1, 2]]
a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
b = [9, 8, 7, 6, 5, 4, 3, 2, 1]

print(list1 == list2)  # false
# print(dict(list1) == dict(list2)) 报错
print(list3 == list4)  # false
print(dict(list3) == dict(list4))  # true
print(dict(list3))
print(a == b)
a = Counter(a)
b = Counter(b)
print(a)
print(b)
print(dict(a) == dict(b))
print(dict(a))

c = copy.deepcopy(list3)
d = copy.deepcopy(list4)
print(c.sort()==d.sort())
print(d)
print(list4)
print(list3.sort() == list4.sort())
print(list3)
print(list4) ##直接用sort list 去比较会高改变ist的值




