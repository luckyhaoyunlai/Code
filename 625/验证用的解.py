from opera import AND
from z3 import *

X,X1,X2=Ints('X X1 X2')


w="pddl1\_Nim\_(2.1-2.3)\Three-piled-nim(v3-le-1).pddl"
e=Not(Or(And(X2==0,X!=X1),And(X2==1,Or(X1-X!=1,X%2==1),Or(X-X1!=1,X1%2==1))))

w="pddl1\_Nim\_(2.1-2.3)\Three-piled-nim(v3-le-2).pddl"
Not(Or(And(X2==0,X!=X1),And(X2==1,Or(X1-X!=1,X%2==1),Or(X-X1!=1,X1%2==1)),
And(X2==2,Or(X-X1!=2,X1%4==2,X1%4==3),Or(X1-X!=2,X%4==2,X%4==3))))

