global c

# c = 0
def plus():
    global c
    a= 1
    b = 2
    c = a + b
    print('在aaa.py 文件中 c 的值是 %d'% c)
    return c

plus()