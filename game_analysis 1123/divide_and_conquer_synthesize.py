from z3 import *


X=Int('X')
Y=Int('Y')
c=Int('c')
d=Int('d')


#常量函数
def Zero():
    return 0
def One():
    return 1
def Two():
    return 2
def Three():
     return 3
def Four(): 
    return 4
def Five():
    return 5
def Six():
    return 6
def Seven():
    return 7
def Eight():
    return 8
def Nine():
    return 9

def Inc(x):
    return x+1
def Dec(x):
    return x-1
def Add(x,y):
    return x+y
def Sub(x,y):
    return x-y
def Mod(x,y):
    return x%y


def Great(x,y):
    return x>y
def Equal(x,y):
    return x==y
def Unequal(x,y):
    return x!=y
def GEqual(x,y):
    return x>=y


def ITE(x:Bool,y,z):
    return y if x else z

#ITE Y和Z的关系式是一样的