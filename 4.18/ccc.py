# stack=[1,2,3,4,5]
# print(stack.pop())
# stack.append(6)
# stack.append(7)
# print(stack)
def funa(): 
    global flag
    flag=2
    funb()
    print("a中被b修改后的：",flag)#3
def funb():
    global flag
    flag=3
    print("b调用a,修改后",flag)#3
funa()
