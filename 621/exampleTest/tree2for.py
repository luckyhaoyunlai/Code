import time
from z3 import *
import copy
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
X=Int('X')
X1=Int('X1')

DT=TreeNode(X%2==0)
DT.left=TreeNode("False")
DT.right=TreeNode(X1%2==0)
DT.right.right=TreeNode("True")
DT.right.left=TreeNode("False")

def tree2Expr(DT) -> str:
    # 结点时术语
    if DT == True: #假设的是pts为空 将树默认设置为True
        return "True"
    expr = ""
    if(type(DT.val)==type("False")):
        # print(DT.val)
        return DT.val
    if (type(DT.val) == type(X == X1)):
        expr = "If("+str(DT.val)+","+tree2Expr(DT.left) +","+tree2Expr(DT.right)+")"
    if(type(DT.val) == type(X) or type(DT.val) == type(0)):
        expr = str(DT.val)
    return expr
def tree2LossingFormula(DT)->str:
    t2ftime = time.time()
    paths=[] #存储一条路径 And(,,,)
    #如果single大于0 那么就 Or(,,,)起来
    stack=[] #python中栈y用数组实现 存放结点
    p=DT
    pre=None
    while(p!=None or len(stack)!=0):
        #到达最左边 p是非空谓词
        while(p!=None and type(p.val)!=type("term")):
            stack.append(p)
            p=p.left
        
        #此时候p一定是叶子结点
        if p !=None and p.val=="True": 
            if len(stack)==1:
                paths.append(stack[0].val)
            else:
                expr="And("
                for i in stack:
                    # print(i.val)
                    expr=expr+str(i.val)+","
                expr=expr[0:len(expr)-1]+")"
                paths.append(expr)
              
        # for i in paths:
        #     print(i)          
        p=stack.pop() #p.left是term
        #如果是叶子结点 且非访问过
        if(type(p.right.val)==type("term") or p.right==pre):
            if(type(p.right.val)==type("term") and p.right.val=="True"):
                p.val=Not(p.val)
                stack.append(p)
                print(len(stack))
                if len(stack)==1:
                    paths.append(stack[0].val)
                else:
                    expr="And("
                    for i in stack:
                        # print(i.val)
                        expr=expr+str(i.val)+","
                    expr=expr[0:len(expr)-1]+")"
                    paths.append(expr)  
                stack=stack[:-1]         
            pre=p
            p=None
        else:
            #非叶子结点
            p.val=Not(p.val)
            stack.append(p)
            p=p.right
    if len(paths)==1:
        print("将树转化成表达式需要的时间：",time.time()-t2ftime)
        return str(paths[0])
    else:
        expr="Or("
        for i in paths:
            expr=expr+str(i)+","
        #会多出一个逗号
        expr=expr[0:len(expr)-1]+")"
    print("将树转化成表达式需要的时间：",time.time()-t2ftime)
    return expr

# def tree2Formula(DT)->str:
#     def bfs(root,path):
#         if not root:return
#         if not root.left and not root.right:
#             #叶子结点为T
#             if root.val=="True":
#                 # print(path)
#                 if len(path)==1:
#                     paths.append(path[0].val)
#                 else:
#                     expr="And("
#                     for i in path:
#                         # print(i.val)
#                         expr=expr+i+","
#                     expr=expr[0:len(expr)-1]+")"
#                     paths.append(expr)            
#         #非叶子结点
#         else:
#             path1=copy.deepcopy(path)
#             path.append(str(root.val))
#             bfs(root.left,path)
#             path1.append(("Not("+str(root.val)+")"))
#             bfs(root.right,path1)
#     paths=[]
#     path=[]
#     bfs(DT,path)
#     if len(paths)==1:
#         return str(paths[0])
#     else:
#         expr="Or("
#         for i in paths:
#             expr=expr+str(i)+","
#         expr=expr[0:len(expr)-1]+")"
#     return expr    


print(tree2Expr(DT))
print(tree2LossingFormula(DT))
# print(simplify(eval(tree2Formula(DT))))