# A=(1,2,3)
# b=[1,2,3,4]
# def fun1(*v):
#     print(v[0])
#     print(v[1])
#     for i in v:
#         print(i)  
# fun1(*A) 
# fun1(1,2,3)
# fun1(*b)

a=1
b=(1,2,3)
c=tuple(a)  #(1,) 1 1
print(len(c)) 
print(c[0])

def fun1(*v):
    print(v)
fun1(*b)  #(1,2,3)
