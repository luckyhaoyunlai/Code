





from z3 import *
x,y,z = Ints('x y z')
s = Solver()
s.add(x>1)
if s.check():
    m = s.model()   
    print(m[x].as_long())
    s.add(x!=m[x].as_long(),y>2)
    if s.check():
        m = s.model()
        print(m[x].as_long(),m[y].as_long())



