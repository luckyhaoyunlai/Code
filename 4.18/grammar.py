from z3 import *


def Add(a, b):
    return a+b


def Sub(a, b):
    return a-b


def Inc(a):
    a = a+1
    return a


def Dec(a):
    a = a - 1
    return a


def Mod(a, b):
    return a % b


def Ge(a, b):
    return a >= b


def Gt(a, b):
    return a > b


def Equal(a, b):
    return a == b


def Unequal(a, b):
    return a != b


def OR(a, b):
    return (a or b)


def z3OR(a, b):
    return Or(a, b)


def AND(a, b):
    return (a and b)


def z3AND(a, b):
    return And(a, b)


def NOT(a):
    return (not a)


def z3NOT(a):
    return Not(a)


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


def ModTest(a, b, c):
    return a % b == c
