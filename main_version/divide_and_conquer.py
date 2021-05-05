# from Winning_strategy_synthesize import ConcreteExs
# from Winning_strategy_synthesize import Add
from enum import Flag
from math import log
from os import pathsep
from re import T
from sys import flags, maxsize
from typing import Type
from z3 import *
import copy
import time

# 运算符号


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


def ITE(c, a, b):
    if(c):
        return a
    else:
        return b


def z3ITE(c, a, b):
    return If(c, a, b)


NUMBER_CONSTANT = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven",
                   8: "Eight", 9: "Nine"}
# (X,X1)--->(Y,Y1)-->TAKE(k_num)
X = Int('X')
Y = Int('Y')
X1 = Int('X1')
Y1 = Int('Y1')
c = Int('c')
d = Int('d')
k_num = Int('k_num')

# Chomp game(2 x n)
actions = [{"action_name": "eat1", "precondition": And(X >= k_num, k_num > 1), "transition_formula": And(And(X >= k_num, k_num > 1), Y == k_num - 1, Implies(X1 >= k_num, Y1 == k_num - 1), Or(X1 >= k_num, Y1 == X1))},
           {"action_name": "eat2", "precondition": And(X1 >= k_num, k_num > 0), "transition_formula": And(And(X1 >= k_num, k_num > 0), Y1 == k_num - 1, Y == X)}]
Game = {"Terminal_Condition": And(X == 1, X1 == 0),
        "actions": actions,
        "Constraint": And(X >= 1, X1 >= 0, X >= X1),
        "var_num": 2,
        "appeal_constants": []} 

p_vocabulary = [{'Input': ['Int', 'Int'], 'Function_name': 'Equal', 'arity': 2},
                # {'Input': ['Int', 'Int'],'Function_name': 'Unequal', 'arity': 2},
                {'Input': ['Int', 'Int'], 'Function_name': 'Ge', 'arity':2},
                {'Input': ['Int', 'Int'], 'Function_name': 'Gt', 'arity':2},
                # {'Input': ['Bool', 'Bool'], 'Function_name': 'OR', 'arity': 2},
                # {'Input': ['Bool', 'Bool'],'Function_name': 'AND', 'arity': 2},
                {'Input': ['Int', 'Int', 'Int'], 'Function_name':'ModTest', 'arity':3}]

t_vocabulary = [{'Input': ['Int', 'Int'],  'Function_name':'Add', 'arity':2},
                {'Input': ['Int', 'Int'], 'Function_name': 'Sub', 'arity':2}, ]
# {'Input': ['Int'], 'Function_name': 'Inc', 'arity':1},
# {'Input': ['Int'], 'Function_name': 'Dec', 'arity':1},
# {'Input': [], 'Function_name': 'Zero', 'arity': 0},
# {'Input': [], 'Function_name': 'One', 'arity': 0},
# {'Input': ['Bool', 'Int', 'Int'], 'Function_name': 'ITE', 'arity': 3}]

# 根据游戏需求，还想加入什么初始值,默认设置为0 1
# for i in Game["appeal_constants"]:
#     t_vocabulary.append({'Input': [], 'Output': 'Int','Function_name': NUMBER_CONSTANT[i], 'arity': 0},)

# 封装所有的函数到FunExg中，之后好调用
FunExg = {'Add': Add, 'Sub': Sub, 'Inc': Inc, 'Dec': Dec, 'Ge': Ge, 'ITE': ITE,
          'Gt': Gt, 'OR': OR, 'AND': AND, 'NOT': NOT, 'Equal': Equal, 'Mod': Mod,
          'Unequal': Unequal, 'X': X, 'Y': Y, 'Zero': Zero, 'One': One, 'ModTest': ModTest}

# if(Game["var_num"] == 2):
#     FunExg['X1'] = X1
#     FunExg['Y1'] = Y1
# for i in Game["appeal_constants"]:
#     FunExg[NUMBER_CONSTANT[i]] = eval(NUMBER_CONSTANT[i])
# Z3FunExg = {'Add': Add, 'Sub': Sub, 'Inc': Inc, 'Dec': Dec, 'Ge': Ge, 'Ite': z3ITE,
#             'Gt': Gt, 'OR': z3OR, 'AND': z3AND, 'NOT': z3NOT, 'Equal': Equal, 'Mod': Mod,
#             'Unequal': Unequal, 'X': X, 'Y': Y, 'Zero': Zero, 'One': One, 'ModTest': ModTest}
# if(Game["var_num"] == 2):
#     Z3FunExg['X1'] = X1
#     Z3FunExg['Y1'] = Y1
# for i in Game["appeal_constants"]:
#     Z3FunExg[NUMBER_CONSTANT[i]] = eval(NUMBER_CONSTANT[i])


"""
按大小枚举谓词
"""
def enumeratePredicate(MaxSize):
    SigSet = []
    ExpSet = []
    SizeOneExps = []
    TempTerms = []

    SizeOneExps.append({'Expression': 0, 'arity': 0, 'size': 1})
    SizeOneExps.append({'Expression': 1, 'arity': 0, 'size': 1})
    SizeOneExps.append({'Expression': X, 'arity': 1, 'size': 1})
    if(Game["var_num"] == 2):
        SizeOneExps.append({'Expression': X1, 'arity': 1, 'size': 1})

    for i in SizeOneExps:
        Goal1 = []
        if (i['arity'] == 0):  # 数字
            for num in range(len(pts)):  # count反例数
                Goal1.append(i['Expression'])
            if Goal1 not in SigSet:  # Sigset标记
                SigSet.append(Goal1)
                i['outputData'] = Goal1
                ExpSet.append(i)  # 表达式添加一个输出项，将表达式加到表达式集合中
        else:
            if i['Expression'] == X:
                for pt in pts:
                    Goal1.append(pt[c])
                if Goal1 not in SigSet:
                    SigSet.append(Goal1)  # SigSet 保留不同的值
                    i['outputData'] = Goal1
                    ExpSet.append(i)  # size_one_表达式 添加到 EXPset
            if i['Expression'] == X1:
                for pt in pts:
                    Goal1.append(pt[d])
                if Goal1 not in SigSet:
                    SigSet.append(Goal1)
                    i['outputData'] = Goal1
                    ExpSet.append(i)
    li = 2
    while (li <= MaxSize):
        for i in t_vocabulary:
            for size1 in range(1, li):
                for choose1 in ExpSet:
                    if(choose1['size'] == size1):
                        for choose2 in ExpSet:
                            if(choose2['size'] == li-size1):
                                term = FunExg[i['Function_name']](
                                    choose1['Expression'], choose2['Expression'])
                                Goal = []  # 计算goal
                                for k, h in zip(choose1['outputData'], choose2['outputData']):
                                    Goal.append(FunExg[i['Function_name']](k, h))
                                if Goal not in SigSet:  # 更新SigSet ExgSet
                                    SigSet.append(Goal)
                                    i['outputData'] = Goal
                                    ExpSet.append({'Expression': term, 'arity': i['arity'], 'outputData': Goal, 'size': MaxSize})

        li = li+1
    
    for i in ExpSet:
        TempTerms.append(i['Expression'])#可以省略的
    # 找出规定大小的terms 从小term枚举到大term 更具这个terms合成preds 小谓词 >= > == != %
    print("枚举谓词需要用到的术语",TempTerms)
    #优化1 如果谓词集合的大小为2^len(pts)则退出 因为已经满足了所有的情况
    #优化2 如果
    #谓词大小 1>x size2  
    predGoal = []
    for i in p_vocabulary:
        if i['arity'] == 2:
            for num1 in range(1,maxsize):
                for num2 in range(1,maxsize):
                    if num1+num2==maxsize:
                        for choose1 in ExpSet:
                            if choose1['size']==num1:
                                for choose2 in ExpSet:
                                    if choose2["size"]==num2:
                                        if str(choose1) != str(choose2):
                                            tempPredicate = FunExg[i['Function_name']](choose1['Expression'], choose2['Expression'])
                                            if str(tempPredicate) != 'False' and str(tempPredicate) != 'True':
                                                goal = []
                                                for pt in pts:
                                                    # print(pt, tempPredicate)
                                                    goal.append(ptSatPred(pt, tempPredicate))
                                                if goal not in predGoal:
                                                    predGoal.append(goal)
                                                    if tempPredicate not in preds:
                                                        preds.append(tempPredicate)
                                                        if len(preds)==pow(2,len(pts)):
                                                            return
        if i['arity']==3:
            for num1 in range(1,maxsize):
                for num2 in range(1,maxsize):
                    for num3 in range(1,maxsize):
                        if num1+num2+num3==maxsize:
                            for choose1 in TempTerms:
                                if choose1["size"]==num1:
                                    for choose2 in TempTerms:
                                        if choose2["size"]==num2:
                                            for choose3 in TempTerms:
                                                if choose3["size"]==num3:
                                                    try:
                                                        tempPredicate = FunExg[i['Function_name']](choose1['Expression'], choose2['Expression'],choose3['Expression'])
                                                        if str(tempPredicate) != 'False' and str(tempPredicate) != 'True':
                                                            goal=[]
                                                            for pt in pts:
                                                                goal.append(ptSatPred(pt,tempPredicate))
                                                            if goal not in predGoal:
                                                                predGoal.append(goal)
                                                                if tempPredicate not in preds:
                                                                    preds.append(tempPredicate)
                                                                    if len(preds)==pow(2,len(pts)):
                                                                        return
                                                    except ZeroDivisionError:  
                                                        pass   

        # if i['arity']==3:
        #     for choose1 in TempTerms:
        #         for choose2 in TempTerms:
        #             for choose3 in TempTerms:
        #                 tempPredicate=FunExg[i['Function_name']](choose1,choose2,choose3):
        #                 #choosee2是否要满足 只能是整数






"""
找到下个term不属于covers的
"""
def nextDistinctTerm():
    ptsLength = len(pts)
    if ptsLength == 0:
        cover[0]=[]
        return  0
    ExpSet = []  # 一轮枚举中枚举的term都但在这里，之后对这个进行运算，枚举更大的term
    SigSet = []
    sizeOneExps = []
    sizeOneExps.append({'Expression': 0, 'arity': 0, 'size': 1})
    sizeOneExps.append({'Expression': 1, 'arity': 0, 'size': 1})
    sizeOneExps.append({'Expression': X, 'arity': 1, 'size': 1})
    sizeOneExps.append({'Expression': X1, 'arity': 1, 'size': 1})
    # 怎么修剪枚举term，怎么设置成已经枚举过了哪个term,还是每次加入pt时都要重新枚举一遍
    # 枚举term
    for i in sizeOneExps:
        if(i['arity'] == 0):  # 枚举 0和1 不需要计算出k
            Goal = []
            term = i['Expression']  # term是取值'Zero'
            for num in range(ptsLength):
                Goal.append(i['Expression'])
            if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                SigSet.append(Goal)
                i['outputData'] = Goal
                ExpSet.append(i)
                # Goal和ptsGoal的匹配 从0匹配到最后一个 求cover[term]
                if term not in terms and term not in cover:
                    for num in range(ptsLength):
                        if(Goal[num] == ptsGoal[num]):
                            if term not in cover:
                                cover[term] = []
                            if pts[num] not in cover[term]:  # 不能重复把点输入cover中
                                cover[term].append(pts[num])
                    # 判断0.1不需要判断cover[term]是否重复了
                    if term in cover:
                        flag = False
                        for t in cover:
                            if(str(t) != str(term) and cover[t] == cover[term]):
                                flag = True
                                break
                        if(flag == False):
                            return term
        else:
            if i['Expression'] == X:
                Goal = []
                term = X
                for pt in pts:
                    Goal.append(pt[c])
                if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                    SigSet.append(Goal)
                    i['outputData'] = Goal
                    ExpSet.append(i)
                    # Goal和ptsGoal的匹配 从0匹配到最后一个 求cover[term]
                    for num in range(ptsLength):
                        if(Goal[num] == ptsGoal[num]):
                            if term not in cover:
                                cover[term] = []
                            if pts[num] not in cover[term]:  # 跟新cover[term]中
                                cover[term].append(pts[num])
                    # 判断cover[term]是否重复了
                    if term in cover and term not in terms:  # 跟新terms
                        flag = False
                        for t in cover:
                            if(str(t) != str(term) and cover[t] == cover[term]):
                                flag = True
                                break
                        if flag == False:
                            return term
            if i['Expression'] == X1:
                Goal = []
                term = X1
                for pt in pts:
                    Goal.append(pt[d])
                if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                    SigSet.append(Goal)
                    i['outputData'] = Goal
                    ExpSet.append(i)
                    # Goal和ptsGoal的匹配 从0匹配到最后一个 求cover[term]
                    for num in range(ptsLength):
                        if(Goal[num] == ptsGoal[num]):
                            if term not in cover:
                                cover[term] = []
                            if pts[num] not in cover[term]:  # 不能重复把点输入cover中
                                cover[term].append(pts[num])
                        # 判断cover[term]是否重复了
                    if term in cover and term not in terms:
                        flag = False
                        for t in cover:
                            if(str(t) != str(term) and cover[t] == cover[term]):
                                flag = True
                                break
                        if(flag == False):
                            return term
    # 上面0 1 ｘ　ｙ已经枚举完了　接下来按大小枚举更大的
    # 设计下自己枚举顺序 先所有的++
    MaxSize = 2
    while(True):
        # 严格按大小枚举term
        # 单纯时term的化是不是不需要t_vocabulary集合
        # 执行add sub 如果还要添加其他的操作再加入vocabulary
        for i in t_vocabulary:
            for size1 in range(1, MaxSize):
                for choose1 in ExpSet:
                    if(choose1['size'] == size1):
                        for choose2 in ExpSet:
                            if(choose2['size'] == MaxSize-size1):
                                term = FunExg[i['Function_name']](choose1['Expression'], choose2['Expression'])
                                Goal = []  # 计算goal
                                for k, h in zip(choose1['outputData'], choose2['outputData']):
                                    Goal.append(
                                        FunExg[i['Function_name']](k, h))
                                if Goal not in SigSet:  # 更新SigSet ExgSet
                                    SigSet.append(Goal)
                                    i['outputData'] = Goal
                                    ExpSet.append({'Expression': term, 'arity': i['arity'], 'outputData': Goal, 'size': MaxSize})
                                    if term not in terms:
                                        # term不在terms才更新cover,且要求最后一个pt必须满足term
                                        for num in range(ptsLength):
                                            if(Goal[num] == ptsGoal[num]):  # 跟新cover[term]
                                                if term not in cover:
                                                    cover[term] = []
                                                if pts[num] not in cover[term]:
                                                    cover[term].append(pts[num])
                                        # 判断cover[term]是否重复了,先判断term是否在cover中
                                        if term in cover and term not in terms:  # 更新terms
                                            flag = False
                                            for t in cover:
                                                if(str(t) != str(term) and cover[t] == cover[term]):
                                                    flag = True
                                                    break
                                            if(flag == False):
                                                return term
        MaxSize += 1


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None



"""
递归合成一颗树
"""
def learn_DT(pts, preds):
    # 递归出口，存在一个term满足所有的pt
    if pts==[]:  #PTS为空不会生成树，设定一颗默认的树
        return TreeNode(X==X)
    for term in terms:
        if not[False for i in pts if i not in cover[term]]:
            # print("叶子结点：",term)
            return TreeNode(str(term))
    if preds == [] or preds == None:
        return None
    Pick_pred = chooseBestPred(pts, preds)
    print("选择最佳谓词", Pick_pred)
    if(Pick_pred==False):  #谓词不足以去划分
        DTflag=False
        return None
    root = TreeNode(Pick_pred)
    ptsYes = []
    ptsNo = []
    for pt in pts:
        if ptSatPred(pt, Pick_pred):
            ptsYes.append(pt)
        else:
            ptsNo.append(pt)
    print(ptsYes, ":", ptsNo)
    temp_preds = copy.deepcopy(preds)
    temp_preds.remove(Pick_pred)
    # print("剩余的谓词",temp_preds)
    root.left = learn_DT(ptsYes, temp_preds)
    root.right = learn_DT(ptsNo, temp_preds)

    return root


def Entropy(pts):
    # print("熵")
    if len(pts) == 0:
        return 0
    entropy = 0.0
    sumcount = 0
    for pt in pts:
        for term in terms:
            if pt in cover[term]:
                sumcount += 1
    for term in terms:
        probability = 0.0
        for pt in pts:
            if pt not in cover[term]:
                probability += 0
            else:
                probability += (1/len(pts))*(count_num_pt(term, pts)/sumcount)
        # print("计算条件概率是", probability)
        if probability != 0:
            entropy -= probability * log(probability, 2)
    # print("熵为", entropy)
    return entropy


# cover(term)覆盖pts点的个数
def count_num_pt(term, pts):
    count = 0
    for pt in pts:
        if pt in cover[term]:
            count += 1
    return count


def chooseBestPred(pts, preds):  # 比较每个pred的信息增益
    Best = {'maxInfoGain': 0, 'predicate': False}
    # print("选择最佳谓词的过程：----")
    # print("谓词集合：",preds)
    # print("pts:",pts)
    for pred in preds:
        ptsYes = []
        ptsNo = []
        # print("谓词：", pred)
        for pt in pts:
            if ptSatPred(pt, pred):
                ptsYes.append(pt)
            else:
                ptsNo.append(pt)
        # print("谓词",pred)
        # print(ptsYes, ":", ptsNo)
        # print((len(ptsYes)/len(pts))*Entropy(ptsYes),
        #       ":", (len(ptsNo)/len(pts))*Entropy(ptsNo))
        InfoGain = Entropy(pts)-(len(ptsYes)/len(pts))*Entropy(ptsYes) -  (len(ptsNo)/len(pts))*Entropy(ptsNo)
        # print("信息增益",InfoGain)
        if InfoGain > Best['maxInfoGain']:
            Best['maxInfoGain'] = InfoGain
            Best['predicate'] = pred

    return Best['predicate']

    # Not(False)


def ptSatPred(pt, pred) -> bool:  # 将pt值代替pred中的未知数
    pred = str(pred)
    # if 'X' in pred:不需要判断，没有得话不会去执行
    pred = pred.replace('X1', str(pt[d]))
    # if 'X1' in pred:
    pred = pred.replace('X', str(pt[c]))
    return eval(pred)

# print(ptSatPred({c: 2, d: 1}, X == X1)) #False
# 根据决策树生成表达式

# DT = TreeNode(X >= X1)
# DT.left = TreeNode(X)
# DT.right = TreeNode(X1 != 0)
# DT.right.left = TreeNode(0)


# DT.right.right = TreeNode(X1)


# 将树转化为表达式
def tree2Expr(DT) -> String:
    
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
#将树转化成Z3表达式
def tree2LossingFormula(DT)->String:
    t2ftime = time.time()
    single=[] #存储一条路径 And(,,,)
    #如果single大于0 那么就 Or(,,,)起来
    stack=[] #python中栈y用数组实现 存放结点
    p=DT
    pre=None
    while(p!=None or len(stack)!=0):
        #到达最左谓词
        while(p!=None and type(p.val)!=type("term")):
            stack.append(p)
            p=p.left
        #输出结果
        if p !=None:
            if len(stack)==1:
                single.append(stack[0].val)
            else:
                expr="And("
                for i in stack:
                    # print(i.val)
                    expr=expr+str(i.val)+","
                expr=expr[0:len(expr)-1]+")"
                single.append(expr)
              
        # for i in single:
        #     print(i)          
        p=stack.pop() #p.left是term
        if(type(p.right.val)==type("term") or p.right==pre):
            pre=p
            p=None
        else:
            p.val=Not(p.val)
            stack.append(p)
            p=p.right

    if len(single)==1:
        print("将树转化成表达式需要的时间：",time.time()-t2ftime)
        return str(single[0])
    else:
        expr="Or("
        for i in single:
            expr=expr+i+","
        expr=expr[0:len(expr)-1]+")"
    print("将树转化成表达式需要的时间：",time.time()-t2ftime)
    return expr

"""
全局转换公式
"""
global_transition_formula = "Exists(k_num,Or("
for i in Game["actions"]:
    global_transition_formula = global_transition_formula +str(i["transition_formula"])+","
global_transition_formula = global_transition_formula+"))"
global_transition_formula = eval(global_transition_formula)

"""
递归得到反例所要使用的点集合
"""
position_1 = []
for i in range(0, 100):
    position_1.append('illegal')

position_2 = []
for i in range(0, 100):
    position_2.append([])
    for j in range(0, 100):
        position_2[i].append('illegal')

"""
设置终态位置状态
"""
s = Solver()
s.add(Game["Terminal_Condition"])
s.check()
m = s.model()
if(Game["var_num"] == 1):
    position_1[m[X].as_long()] = True
if(Game["var_num"] == 2):
    position_2[m[X].as_long()][m[X1].as_long()] = True


# 接受*个参数的元组 递归判断是否是lossing_state
def isLossingState(*v):  # 接受1或者2个参数的元组 根据终结条件去判断是否是lossing_state
    timeisLossingstate=time.time()
    if (len(v) == 1):
        if (position_1[v[0]] != 'illegal'):
            print("判断PN态所需要的时间：",time.time()-timeisLossingstate)
            return position_1[v[0]]
        for x in range(0, v[0] + 1):
            if (position_1[x] != 'illegal'):
                continue
            temp = []
            while (True):
                s = Solver()
                s.add(global_transition_formula)
                s.add(Game["Constraint"])
                s.add(X == x)
                for i in temp:
                    s.add(Or(Y != i[0]))
                if (s.check() == sat):
                    m = s.model()
                    temp.append([m[Y].as_long()])
                else:
                    break
            is_losing = True
            s = Solver()
            s.add(Game["Constraint"])
            s.add(X == x)
            if (s.check() == unsat):
                continue
            for i in temp:
                if (position_1[i[0]] == 'illegal'):
                    position_1[i[0]] = isLossingState(i[0])
            for i in temp:
                is_losing = is_losing and not position_1[i[0]]
            if (is_losing):
                position_1[x] = True
            else:
                position_1[x] = False
        print("判断PN态所需要的时间：",time.time()-timeisLossingstate)
        return position_1[v[0]]

    if(len(v) == 2):
        if(position_2[v[0]][v[1]] != 'illegal'):  # 已经访问过了的，直接访问值，没有的
            return position_2[v[0]][v[1]]
        for x in range(0, v[0]+1):  # 遍历所有的点去设置状态
            for y in range(0, v[1]+1):
                if(position_2[x][y] != 'illegal'):
                    continue
                temp = []  # 存放转移后的解 y y1即执行动作后的值
                while (True):
                    s = Solver()
                    s.add(global_transition_formula)
                    s.add(Game["Constraint"])
                    s.add(X == x, X1 == y)

                    for i in temp:
                        s.add(Or(Y != i[0], Y1 != i[1]))

                    if (s.check() == sat):
                        m = s.model()
                        temp.append([m[Y].as_long(), m[Y1].as_long()])  # 全局转移解
                    else:
                        break

                # print('438',temp) 存放状态 438 [[2, 1], [2, 0], [1, 1]]
                is_losing = True
                s = Solver()
                s.add(Game["Constraint"])
                s.add(X == x, X1 == y)
                if(s.check() == unsat):
                    continue
                for i in temp:
                    if(position_2[i[0]][i[1]] == 'illegal'):
                        position_2[i[0]][i[1]] = isLossingState(i[0], i[1])
                for i in temp:
                    is_losing = is_losing and not position_2[i[0]][i[1]]
                if (is_losing):
                    position_2[x][y] = True
                else:
                    position_2[x][y] = False
        print("判断PN态所需要的时间：",time.time()-timeisLossingstate)
        return position_2[v[0]][v[1]]


# 遍历出一个不在反例集合中的点满足约束但是不满足候选表达式
def FindCountExample(expr):
    if (Game["var_num"] == 1):
        i = 2
        while(True):
            for v1 in range(0, i):
                flag12 = False
                for pt in pts:
                    if (v1 == pt[c]):
                        flag12 = True
                if flag12 == False:
                    s = Solver()
                    s.add(Game["Constraint"])
                    s.add(X == v1)
                    if (s.check() == sat):
                        return v1
                    else:
                        continue
            i = i + 1
    if(Game["var_num"] == 2):
        i = 2
        while(True):
            for v1 in range(0, i):
                for v2 in range(0, i):
                    if v1+v2 == i:  # 遍历所有的v1v2=i的组合 按照size遍历
                        flag12 = False
                        # 改成 pt={c:v1,d:v2} if pt not in pts:
                        for pt in pts:
                            if (v1 == pt[c] and v2 == pt[d]):
                                flag12 = True
                        if flag12 == False:  # 不在反例集合中
                            s = Solver()
                            s.add(Game["Constraint"])  # 满足约束条件
                            s.add(X == v1, X1 == v2)
                            # if(s.check()==sat):
                            #     return v1,v2
                            # else continue
                            # 要求设置成不满足expr
                            if(s.check() == sat):
                                # print(expr)
                                # 要求在这里就设置为反例
                                # print("该轮枚举：", v1, v2)
                                boolTemp = isLossingState(v1, v2)
                                boolTemp2 = eval(str(expr).replace(str(X1), str(v2)).replace(str(X), str(v1)))
                                s = Solver()
                                if boolTemp == False:
                                    s.add(True, boolTemp2)
                                    if(s.check() == sat):
                                        return v1, v2
                                elif boolTemp == True:
                                    s.add(True, boolTemp2)
                                    if(s.check() == unsat):
                                        return v1, v2
                            else:
                                continue
            i = i+1


def exampleOutput(specifition):  # 输入pt 输出结果

    return 0


def isCoverAll():
    coverAll = []
    for term in terms:
        for i in cover[term]:
            coverAll.append(i)
    # print("cover包含的所有的点",coverAll)
    for pt in pts:
        if pt not in coverAll:
            return False
    return True

   

start_winning_formula_time = time.time()
#合成必败公式
pts=[]
ptsGoal=[]
while(True):
    terms=[True,False]
    cover={}
    preds=[]
    cover[True]=[]
    cover[False]=[]
    DT=None
    
    #所有的点都加入cover中
    for num in range(len(pts)):
        cover[ptsGoal[num]].append(pts[num])
    print("cover集合：",cover)

    # while(not(isCoverAll())):
    #     terms=terms.append(nextDistinctTerm())
    DTflag=True
    e=X==X  #默认表达式
    maxsize=2
    DTTime=time.time()
    while(pts!= [] and (DT==None or  DTflag==False)):
        DTflag=True
        enumPredsTime=time.time()
        enumeratePredicate(maxsize)
        print("枚举谓词所用的时间：",time.time()-enumPredsTime)
        print("术语",terms)
        print("谓词",preds)
        print("反例集合",pts)
        calculateIGTime=time.time()
        DT=learn_DT(pts,preds)  #lenrnDT中可能会出现 找出不了最好的谓词划分
        print("计算信息增益的时间是：",time.time()-calculateIGTime)
        print(DTflag)
        if(DTflag==False):
            print('不能划分')
            maxsize+=1
    print("合成DT需要的时间：",time.time()-DTTime) 
    tree2Exprtime=time.time()
    if DT!=None :e = eval(tree2Expr(DT)) 
    print("树转化成条件表达式时间：",time.time()-tree2Exprtime)
    print("枚举的决策树：",e)
    e1=eval(str(e).replace("X1","Y1").replace("X","Y"))
    s=Solver()
    smttime=time.time()
    s.add(Or(And(Game["Terminal_Condition"], Not(e)),  # 必败态公式 是定义7的取反 
             Not(Implies(And(e, Game["Constraint"]), ForAll([Y, Y1], Implies(global_transition_formula, Not(e1))))),
             Not(Implies(And(Not(e), Game["Constraint"]), Exists([Y, Y1], And(global_transition_formula, e1))))))
    if(s.check()==unsat):
        print("SMT判断所用时间：",time.time()-smttime)
        # losing_formula = e
        lossing_formula=eval(tree2LossingFormula(DT))
        losing_formula_Y = e1
        print("-----------------------------")
        winning_formula_time = time.time()-start_winning_formula_time
        
        print("必胜公式是：",Not(lossing_formula))
        print("花费的时间是：",winning_formula_time)
        break
    else:
        if (Game["var_num"] == 1):
            num4 = FindCountExample(e)
        if (Game["var_num"] == 2):
            num4, num5 = FindCountExample(e)
    if (Game["var_num"] == 1):
        if {c: num4} not in pts:
            pts.append({c: num4})
            ptsGoal.append(isLossingState(num4))
          
    if (Game["var_num"] == 2):
        if {c: num4, d: num5} not in pts:
            pts.append({c: num4, d: num5})
            ptsGoal.append(isLossingState(num4,num5))
           
             

    # s.add(Or(And(Game["Terminal_Condition"], Not(e[0])),  # 必败态公式 是定义7的取反
    #          Not(Implies(And(e[0], Game["Constraint"]), ForAll(
    #              [Y, Y1], Implies(global_transition_formula, Not(e[1]))))),
    #          Not(Implies(And(Not(e[0]), Game["Constraint"]), Exists([Y, Y1], And(global_transition_formula, e[1]))))))


# pts=[]  # 点集
# goal=[]  # 结果集合
# ptsGoal=[]
# while True:
#     terms=[0]
#     preds=[]
#     cover={}
#     DT=None

# #     # 使covers完全覆盖pts的output

#     while DT == None:
#         terms.append(nextDistinctTerm())  # 要使cover完全覆盖pts
#         preds.append(enumeratePredicate())
#         DT=learn_DT(terms, preds)
#     # DT的表达式一定会满足全部反例? code还未写

#         e=tree2Expr(DT)
#         specificationTemp=copy.deepcopy(specification)#游戏规则可以替换掉了
#         specificationTemp=eval(str(specificationTemp).replace(str(k_num), '('+str(e)+')'))  # 枚举的结果代替要求的未知数

#         s=Solver()
#         s.add(Not(specificationTemp))  # 取反，为了能直接用solver求countexample
#         if s.check() == unsat:
#             print("枚举成功")
#             break
#         else:
#             m=s.model()
#             num1=m[X].as_long()  # "如果规范中不是两个位置参数，到时再分类，有几个参数分几类"
#             num2=m[Y].as_long()
#         # num1 num2可不可能已经出现在pts中？？

#         # 得到的反例去求pts
#         specificationTemp=copy.deepcopy(specification)
#         specificationTemp=eval(str(specificationTemp).replace(
#             str(X), '('+str(num1)+')').replace(str(Y), '('+str(num2)+')'))
#         result=exampleOutput(specificationTemp)

#         if({"Input": {c: num1, d: num2}, 'Outout': result})not in pts:  # 先假设只要两个未知数，到时加上
#             pts.append({"Input": {c: num1, d: num2}, 'Outout': result})
#             # 如果叶子结点时bool类型呢？  cover就是goal 有类型有value
#             goal.append(result)  # 所有的pt对应的点
#             cover['value'].append(result)





# e_num = Int('e_num')
# specification = And(e_num >= X, e_num >= X1, Or(e_num == X, e_num == X1))


# pts = []
# ptsGoal = []
# terms = [True,False]
# cover = {True:[],False:[]}
# preds = []

# enumeratePredicate(1)
# print("terms", terms)
# print("cover", cover)
# print(preds)

# DT = learn_DT(pts, preds)
# a = tree2Expr(DT)
# print(a)

# pts.append({c: 1, d: 1})
# ptsGoal.append(False)
# cover[ptsGoal[-1]].append(pts[-1])

# enumeratePredicate(1)
# print("terms", terms)
# print("cover", cover)
# print("preds", preds)
# DT = learn_DT(pts, preds)
# a = tree2Expr(DT)
# print(a)

# pts.append({c: 2, d: 1})
# ptsGoal.append(True)
# cover[ptsGoal[-1]].append(pts[-1])
# enumeratePredicate(1)
# print("terms", terms)
# print("cover", cover)
# print("preds", preds)
# DT = learn_DT(pts, preds)
# a = tree2Expr(DT)
# print(a)


# pts.append({c: 3, d: 1})
# ptsGoal.append(False)
# cover[ptsGoal[-1]].append(pts[-1])
# enumeratePredicate(1)
# print("terms", terms)
# print("cover", cover)
# print("preds", preds)
# DT = learn_DT(pts, preds)
# a = tree2Expr(DT)
# print(a)

