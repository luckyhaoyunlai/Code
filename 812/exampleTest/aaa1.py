from exampleTest.aaa import c

def plus():
    e = 1
    f = c + e
    print('在bbb.py 文件中 c 的值是 %d'% c)
    print('f 的值是 %d'% f)
    return f

plus()