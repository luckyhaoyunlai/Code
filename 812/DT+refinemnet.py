import threading
import eventlet
from pkg_resources import NullProvider, SOURCE_DIST
import xlrd
from subfile.PDDLGrammarLexer import PDDLGrammarLexer
from subfile.PDDLGrammarParser import PDDLGrammarParser
from math import log
from z3 import *
from MyVisitor import Item, MyVisitor
from MyVisitor import game
from opera import *
from antlr4 import *
import time
from xlwt import *
from xlrd import *
from xlutils.copy import copy
from copy import deepcopy as deepcopy

X = Int('X')
X1 = Int('X1')
X2 = Int('X2')
Y = Int('Y')
Y1 = Int('Y1')
Y2 = Int("Y2")

k = Int('k')
l = Int('l')
(k1, k2, k3) = Ints('k1 k2 k3')

ptk = 30
ptk2 = 15
"""=================game import========================="""
# pddlFile =sys.argv[1] #由文件main.py输入路径
# resultFile =sys.argv[2]
pddlFile = r"pddl3\_Nim\CircularNim(3,3,v_3-1).pddl"  # 执行单个pddl
resultFile = r"C:\Users\admin\Desktop\result\8_7.xls"  # 生成的结果文件

oldwb = xlrd.open_workbook(resultFile, encoding_override='utf-8')
sheet1 = oldwb.sheet_by_index(0)
row = sheet1.nrows



input_stream = FileStream(pddlFile)
lexer = PDDLGrammarLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = PDDLGrammarParser(token_stream)
tree = parser.domain()
visitor = MyVisitor()
visitor.visit(tree)

Terminal_Condition = eval(str(game.tercondition).replace(
    'v1', 'X').replace('v2', 'X1').replace('v3', 'X2'))
Constarint = eval(str(game.constraint).replace(
    'v1', 'X').replace('v2', 'X1').replace('v3', 'X2'))
varList = []
for i in game.var_list:
    i = str(i).replace('v1', 'X').replace('v2', 'X1').replace('v3', 'X2')
    varList.append(eval(i))
actions = []


for i in game.action_list:
    one = {"action_name": i[0],
           "action_parameter": i[1],
           "precondition": eval(str(i[2]).replace('v1', 'X').replace('v2', 'X1').replace('v3', 'X2')),
           "transition_formula": eval(str(i[3]).replace('v1\'', 'Y').replace('v2\'', 'Y1').replace('v3\'', 'Y2').replace('v3', 'X2').replace('v1', 'X').replace('v2', 'X1'))}
    actions.append(one)

Game = {"Terminal_Condition": Terminal_Condition,
        "varList": varList,
        "actions": actions,
        "Constraint": Constarint,
        "var_num": game.objectsCount,
        "type": "normal",
        "appeal_constants": game.constantList}

print("Var List:",varList)
varListY = eval(str(varList).replace('X2','Y2').replace('X1','Y1').replace('X','Y'))
print("Var Y list",varListY)


print("appeal constant", Game['appeal_constants'])
print("================================================================")
"""=============================================================================="""

p_vocabulary = [{'Input': ['Int', 'Int'], 'Function_name': 'Equal', 'arity': 2},
                {'Input': ['Int', 'Int'], 'Function_name': 'Ge', 'arity':2},
                {'Input': ['Int', 'Int'], 'Function_name': 'Gt', 'arity':2},
                {'Input': ['Int', 'Int', 'Int'], 'Function_name':'ModTest', 'arity':3}]

t_vocabulary = [{'Input': ['Int', 'Int'],  'Function_name':'Add', 'arity':2},
                {'Input': ['Int', 'Int'], 'Function_name': 'Sub', 'arity':2}, ]

FunExg = {'Add': Add, 'Sub': Sub, 'Inc': Inc, 'Dec': Dec, 'Ge': Ge, 'ITE': ITE,
          'Gt': Gt, 'OR': OR, 'AND': AND, 'NOT': NOT, 'Equal': Equal, 'Mod': Mod,
          'Unequal': Unequal, 'X': X, 'Y': Y, 'Zero': Zero, 'One': One, 'ModTest': ModTest}


#interResult of enumerate
class InterResult:
    def __init__(self,expSet,sigSet) -> None:
        self.SigSet = sigSet
        self.ExpSet = expSet
interResultPred = InterResult("","") 
interResultTerm = InterResult("","") 

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

"""按大小枚举谓词"""
def enumeratePredicate(MaxSize,DTFlag):
    global interResultPred
    SigSet = []
    ExpSet = []
    SizeOneExps = []
    Items = []
    ItemsNum = []
    ItemsVar = []
    if DTFlag:
        SizeOneExps.append({'Expression': 0, 'Isnum': True, 'size': 1})
        SizeOneExps.append({'Expression': 1, 'Isnum': True, 'size': 1})
        SizeOneExps.append({'Expression': X, 'Isnum': False, 'size': 1})
        for i in Game["appeal_constants"]:
            SizeOneExps.append({'Expression': eval(i), 'Isnum': True, 'size': 1})
        if Game["var_num"] == 2:
            SizeOneExps.append({'Expression': X1, 'Isnum': False, 'size': 1})
        elif Game["var_num"] == 3:
            SizeOneExps.append({'Expression': X1, 'Isnum': False, 'size': 1})
            SizeOneExps.append({'Expression': X2, 'Isnum': False, 'size': 1})

        for i in SizeOneExps:
            Goal1 = []
            if (i['Isnum']):  # 数字
                for num in range(len(pts)):  # count反例数
                    Goal1.append(i['Expression'])
                if Goal1 not in SigSet:  # Sigset标记
                    SigSet.append(Goal1)
                    i['outputData'] = Goal1
                    ExpSet.append(i)  # 表达式添加一个输出项，将表达式加到表达式集合中
            else:
                if i['Expression'] == X:
                    for pt in pts:
                        Goal1.append(pt[0])
                    if Goal1 not in SigSet:
                        SigSet.append(Goal1)  # SigSet 保留不同的值
                        i['outputData'] = Goal1
                        ExpSet.append(i)  # size_one_表达式 添加到 EXPset
                if i['Expression'] == X1:
                    for pt in pts:
                        Goal1.append(pt[1])
                    if Goal1 not in SigSet:
                        SigSet.append(Goal1)
                        i['outputData'] = Goal1
                        ExpSet.append(i)
                if i['Expression'] == X2:
                    for pt in pts:
                        Goal1.append(pt[2])
                    if Goal1 not in SigSet:
                        SigSet.append(Goal1)
                        i['outputData'] = Goal1
                        ExpSet.append(i)
    
    li = 2
    if DTFlag == False: #表示在生成树失败，需要借助上一次枚举的结果继续往下枚举
        SigSet = interResultPred.SigSet
        ExpSet = interResultPred.ExpSet
        li = MaxSize
    while li <= MaxSize:
        for i in t_vocabulary:
            if i['Function_name'] == 'Add':
                if li <= 3:  # add(var,-)
                    for size1 in range(1, li):
                        for choose1 in ExpSet:
                            # 修枝 sub第一个参数必须非num
                            if choose1['size'] == size1 and choose1['Isnum'] == False:
                                for choose2 in ExpSet:
                                    if choose2['size'] == li-size1:
                                        term = FunExg[i['Function_name']](
                                            choose1['Expression'], choose2['Expression'])
                                        Goal = []
                                        for k1, h in zip(choose1['outputData'], choose2['outputData']):
                                            Goal.append(
                                                FunExg[i['Function_name']](k1, h))
                                        if Goal not in SigSet:
                                            SigSet.append(Goal)
                                            i['outputData'] = Goal
                                            ExpSet.append(
                                                {'Expression': term, 'Isnum': False, 'outputData': Goal, 'size': li})
                for size1 in range(1, li):  # add(num,num)
                    for choose1 in ExpSet:
                        if choose1['size'] == size1 and choose1['Isnum'] == True:
                            for choose2 in ExpSet:
                                if choose2['size'] == li-size1 and choose2['Isnum']:
                                    term = FunExg[i['Function_name']](
                                        choose1['Expression'], choose2['Expression'])
                                    Goal = []
                                    for k1, h in zip(choose1['outputData'], choose2['outputData']):
                                        Goal.append(
                                            FunExg[i['Function_name']](k1, h))
                                    if Goal not in SigSet:  # 更新SigSet ExgSet
                                        SigSet.append(Goal)
                                        i['outputData'] = Goal
                                        ExpSet.append(
                                            {'Expression': term, 'Isnum': choose1['Isnum'] and choose2['Isnum'], 'outputData': Goal, 'size': li})
            elif i['Function_name'] == 'Sub':
                if li <= 3:  # 自己修枝sub 只有li=2时出现
                    for size1 in range(1, li):
                        for choose1 in ExpSet:
                            # 修枝 sub第一个参数必须非num
                            if choose1['size'] == size1 and choose1['Isnum'] == False:
                                for choose2 in ExpSet:
                                    if choose2['size'] == li - size1 and str(choose1['Expression']) != str(choose2['Expression']):
                                        term = FunExg[i['Function_name']](
                                            choose1['Expression'], choose2['Expression'])
                                        Goal = []
                                        for k1, h in zip(choose1['outputData'], choose2['outputData']):
                                            Goal.append(
                                                FunExg[i['Function_name']](k1, h))
                                        if Goal not in SigSet:
                                            SigSet.append(Goal)
                                            i['outputData'] = Goal
                                            ExpSet.append(
                                                {'Expression': term, 'Isnum': False, 'outputData': Goal, 'size': li})
        li += 1
    interResultPred = InterResult(ExpSet,SigSet)
    for i in ExpSet:
        Items.append(i['Expression'])
        if i['Isnum']:
            ItemsNum.append(i)
        else:
            ItemsVar.append(i)
    print("Items set generate predicate:\n\t", Items)

    # 优化1 如果谓词集合的大小为2^len(pts)则退出 因为已经满足了所有的情况
    # 优化2 如果
    # maxsize=MaxSize+1
    predGoal = []
    for i in p_vocabulary:  # == > >=
        if i['arity'] == 2:
            for choose1 in ItemsVar:
                for choose2 in ItemsVar:
                    if choose2 != choose1 and choose2["size"] <= 4 - choose1["size"]:#设置
                            tempPredicate = FunExg[i['Function_name']](
                                choose1['Expression'], choose2['Expression'])
                            if str(tempPredicate) != 'False' and str(tempPredicate) != 'True':
                                goal = []
                                for pt in pts:
                                    goal.append(ptSatPred(pt, tempPredicate))
                                if goal not in predGoal:
                                    predGoal.append(goal)
                                    if tempPredicate not in preds:
                                        preds.append(tempPredicate)
                                        if len(preds) == pow(2, len(pts)):
                                            return
                for choose2 in ItemsNum:
                    tempPredicate = FunExg[i['Function_name']](
                        choose1['Expression'], choose2['Expression'])
                    if str(tempPredicate) != 'False' and str(tempPredicate) != 'True':
                        goal = []
                        for pt in pts:
                            goal.append(ptSatPred(pt, tempPredicate))
                        if goal not in predGoal:
                            predGoal.append(goal)
                            if tempPredicate not in preds:
                                preds.append(tempPredicate)
                                if len(preds) == pow(2, len(pts)):
                                    return
        if i['arity'] == 3:
            for choose1 in ItemsVar:
                for choose2 in ItemsNum:
                    for choose3 in ItemsNum:
                        if choose3["Expression"]<choose2["Expression"]:
                            try:
                                tempPredicate = FunExg[i['Function_name']](
                                    choose1["Expression"], choose2["Expression"], choose3["Expression"])
                                if str(tempPredicate) != 'False' and str(tempPredicate) != 'True':
                                    goal = []
                                    for pt in pts:
                                        goal.append(ptSatPred(pt, tempPredicate))
                                    if goal not in predGoal:
                                        predGoal.append(goal)
                                        if tempPredicate not in preds:
                                            preds.append(tempPredicate)
                                            if len(preds) == pow(2, len(pts)):
                                                return
                            except ZeroDivisionError:
                                pass


"""输出某个pt下的最小size的term
eg. pt[[3,3],[1,3]] term =[1,V1]
eg pt = [5,1] output = [0,3] """
def enumerateTerm(pt,ptGoal):
    ExpSet = []
    SigSet = []
    sizeOneExps = []
    # var_num 之后修改 - 先设置好两个变量的
    sizeOneExps.append({'Expression': 0, 'arity': 0, 'size': 1})
    sizeOneExps.append({'Expression': 1, 'arity': 0, 'size': 1})
    sizeOneExps.append({'Expression': X, 'arity': 1, 'size': 1})
    if Game["var_num"] == 2:
        sizeOneExps.append({'Expression': X1, 'arity': 1, 'size': 1})
    if Game["var_num"] == 3:
        sizeOneExps.append({'Expression': X1, 'arity': 1, 'size': 1})
        sizeOneExps.append({'Expression': X2, 'arity': 1, 'size': 1})
    for i in sizeOneExps:
        if i['arity']==0:
            term = i['Expression']
            if term not in SigSet:
                SigSet.append(term)
                i['outputData'] = term
                ExpSet.append(i)
                if term == ptGoal:
                    return term
        if i['Expression'] == X:
            term = X
            Goal = pt[0]
            if Goal not in SigSet:
                SigSet.append(Goal)
                i['outputData'] = Goal
                ExpSet.append(i)
                if Goal == ptGoal:
                    return term
        if i['Expression'] == X1:
            term = X1
            Goal = pt[1]
            if Goal not in SigSet:
                SigSet.append(Goal)
                i['outputData'] = Goal
                ExpSet.append(i)
                if Goal == ptGoal:
                    return term
        if i['Expression'] == X2:
            term = X2
            Goal = pt[2]
            if Goal not in SigSet:
                SigSet.append(Goal)
                i['outputData'] = Goal
                ExpSet.append(i)
                if Goal == ptGoal:
                    return term
    sizeT = 2
    while True:
        ##之后补充修枝
        for i in t_vocabulary :
            for size1 in range(1,sizeT):
                for choose1 in ExpSet:
                    if choose1['size']== size1:
                        for choose2 in ExpSet:
                            if choose2['size'] == sizeT - size1:
                                term = FunExg[i['Function_name']](choose1['Expression'],
                                         choose2['Expression'])
                                Goal = FunExg[i['Function_name']](choose1['outputData'],
                                         choose2['outputData'])
                                if Goal == ptGoal:
                                    return term
                                if Goal not in SigSet:
                                    SigSet.append(Goal)
                                    i['outputData'] = Goal
                                    ExpSet.append({'Expression': term, 'arity': i['arity'], 'outputData': Goal, 'size': sizeT})
        sizeT += 1

"""找到size的term不属于cover的满足某pt的 动作参数只有一个""" 
def nextSize1Term(termMaxSize,DTFlag):
    print("next size of term:",termMaxSize)
    global interResultTerm
    flagHaveTerm = False
    ExpSet = []  # 一轮枚举中枚举的term都但在这里，之后对这个进行运算，枚举更大的term
    SigSet = []
    # 怎么修剪枚举term，怎么设置成已经枚举过了哪个term,还是每次加入pt时都要重新枚举一遍
    # 枚举term
    if  DTFlag:
        sizeOneExps = []
        sizeOneExps.append({'Expression': 0,'Isnum':True, 'arity': 0, 'size': 1})
        sizeOneExps.append({'Expression': 1,'Isnum':True, 'arity': 0, 'size': 1})
        sizeOneExps.append({'Expression': X,'Isnum':False,'arity': 1, 'size': 1})
        if Game["var_num"] == 2:
            sizeOneExps.append({'Expression': X1,'Isnum':False, 'arity': 1, 'size': 1})
        elif Game["var_num"] == 3:
            sizeOneExps.append({'Expression': X1, 'Isnum': False, 'size': 1})
            sizeOneExps.append({'Expression': X2, 'Isnum': False, 'size': 1})
        for i in Game["appeal_constants"]:
            sizeOneExps.append({'Expression': eval(i), 'Isnum': True, 'size': 1})
        for i in sizeOneExps:
            if i['Isnum'] :  # 枚举 0和1 不需要计算出k
                Goal = []
                term = i['Expression']  
                for num in range(len(pts)):
                    Goal.append(i['Expression'])
                if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                    SigSet.append(Goal)
                    i['outputData'] = Goal
                    ExpSet.append(i)
                    # Goal和ptsGoal的匹配 从0匹配到最后一个 求cover[term]
                    # if term not in terms and term not in cover:
                    for actNum in range(len(actions)):
                        Term = (actNum,term)
                        if Term not in cover:
                            coverTemp = []
                            for num in range(len(pts)): #判断所有的点有多少个满足pt
                                pt = pts[num]
                                ptOutput = ptsOutput[num]
                                for output in ptOutput: # 一个input对应多个output
                                    if output[0] == actNum and Goal[num] == output[1]:
                                        coverTemp.append(pt)
                                        break
                            if coverTemp != []:
                                flag = False
                                for t in cover:
                                    if len(cover[t]) == len(coverTemp):
                                        list1 = deepcopy(cover[t])
                                        list2 = deepcopy(cover[t])
                                        if list1.sort() == list2.sort():
                                            flag = True
                                            break
                                if(flag == False):
                                    terms.append(Term)
                                    cover[Term]=coverTemp
                        
                                    # flagHaveTerm = True
                                    # return 
            else:
                if i['Expression'] == X:
                    Goal = []
                    term = X
                    for pt in pts:
                        Goal.append(pt[0])
                    if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                        SigSet.append(Goal)
                        i['outputData'] = Goal
                        ExpSet.append(i)
                        # Goal和ptsOutput的匹配 从0匹配到最后一个 求cover[term]
                        for actNum in range(len(actions)):
                            Term = (actNum,term)
                            if Term not in cover:
                                coverTemp = []
                                for num in range(len(pts)):
                                    pt = pts[num]
                                    ptOutput = ptsOutput[num]                                
                                    for output in ptOutput:
                                        if output[0] ==actNum and Goal[num] == output[1]:
                                            coverTemp.append(pt)
                                # 判断cover[term]是否重复了
                                if coverTemp != []:
                                    flag = False
                                    for t in cover:
                                        if len(cover[t]) == len(coverTemp):
                                            list1 = deepcopy(cover[t])
                                            list2 = deepcopy(cover[t])
                                            if list1.sort() == list2.sort():
                                                flag = True
                                                break
                                    if(flag == False):
                                        terms.append(Term)
                                        cover[Term] = coverTemp
                    
                                        # flagHaveTerm = True
                                        # return 
                if i['Expression'] == X1:
                    Goal = []
                    term = X1
                    for pt in pts:
                        Goal.append(pt[1])
                    if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                        SigSet.append(Goal)
                        i['outputData'] = Goal
                        ExpSet.append(i)
                        # Goal和ptsOutput的匹配 从0匹配到最后一个 求cover[term]
                        for actNum in range(len(actions)):
                            Term = (actNum,term)
                            if Term not in cover:
                                coverTemp = []
                                for num in range(len(pts)):
                                    pt = pts[num]
                                    ptOutput = ptsOutput[num]                                
                                    for output in ptOutput:
                                        if output[0] ==actNum and Goal[num] == output[1]:
                                            coverTemp.append(pt)
                                # 判断cover[term]是否重复了
                                if coverTemp != []:
                                    flag = False
                                    for t in cover:
                                        if len(cover[t]) == len(coverTemp):
                                            list1 = deepcopy(cover[t])
                                            list2 = deepcopy(cover[t])
                                            if list1.sort() == list2.sort():
                                                flag = True
                                                break
                                    if(flag == False):
                                        terms.append(Term)
                                        cover[Term] = coverTemp

                if i['Expression'] == X2:
                    Goal = []
                    term = X2
                    for pt in pts:
                        Goal.append(pt[2])
                    if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                        SigSet.append(Goal)
                        i['outputData'] = Goal
                        ExpSet.append(i)
                        # Goal和ptsOutput的匹配 从0匹配到最后一个 求cover[term]
                        for actNum in range(len(actions)):
                            Term = (actNum,term)
                            if Term not in cover:
                                coverTemp = []
                                for num in range(len(pts)):
                                    pt = pts[num]
                                    ptOutput = ptsOutput[num]                                
                                    for output in ptOutput:
                                        if output[0] ==actNum and Goal[num] == output[1]:
                                            coverTemp.append(pt)
                                # 判断cover[term]是否重复了
                                if coverTemp != []:
                                    flag = False
                                    for t in cover:
                                        if len(cover[t]) == len(coverTemp):
                                            list1 = deepcopy(cover[t])
                                            list2 = deepcopy(cover[t])
                                            if list1.sort() == list2.sort():
                                                flag = True
                                                break
                                    if(flag == False):
                                        terms.append(Term)
                                        cover[Term] = coverTemp
                            
                                        # flagHaveTerm = True
                                        # return
        # if flagHaveTerm == False: 
            # termMaxSize += 1
    li = 2
    if DTFlag == False:
        SigSet = interResultTerm.SigSet
        ExpSet = interResultTerm.ExpSet
        li = termMaxSize
    print("")
    while li <= termMaxSize:
        for i in t_vocabulary:
            if i['Function_name'] == 'Add':
                if li <= 3:  #add(var,-)
                    for size1 in range(1, li):
                        for choose1 in ExpSet:
                            if choose1['size'] == size1 and choose1['Isnum'] == False:
                                for choose2 in ExpSet:
                                    if choose2['size'] == li-size1:
                                        term = FunExg[i['Function_name']](
                                            choose1['Expression'], choose2['Expression'])
                                        # print("计算得term505",term)
                                        Goal = []  # 计算goal
                                        for k1, h in zip(choose1['outputData'], choose2['outputData']):
                                            Goal.append(FunExg[i['Function_name']](k1, h))
                                        if Goal not in SigSet:  # 更新SigSet ExgSet
                                            SigSet.append(Goal)
                                            i['outputData'] = Goal
                                            ExpSet.append({'Expression': term, 'Isnum': False,'arity': i['arity'], 
                                                        'outputData': Goal, 'size': li})
                                            for actNum in range(len(actions)):
                                                Term = (actNum,term)
                                                if Term not in cover:
                                                    coverTemp = []
                                                    for num in range(len(pts)):
                                                        pt = pts[num]
                                                        ptOutput = ptsOutput[num]                                
                                                        for output in ptOutput:
                                                            if output[0] ==actNum and Goal[num] == output[1]:
                                                                coverTemp.append(pt)
                                                    # 判断cover[term]是否重复了
                                                    if coverTemp != []:
                                                        flag = False
                                                        for t in cover:
                                                            if len(cover[t]) == len(coverTemp):
                                                                list1 = deepcopy(cover[t])
                                                                list2 = deepcopy(cover[t])
                                                                if list1.sort() == list2.sort():
                                                                    flag = True
                                                                    break
                                                        if(flag == False):
                                                            terms.append(Term)
                                                            cover[Term] = coverTemp
                                                            flagHaveTerm = True
                                                            # return
                for size1 in range(1,li): #add(num,num)
                    for choose1 in ExpSet:
                        if choose1['size'] == size1 and choose1['Isnum'] :
                            for choose2 in ExpSet:
                                if choose2['size'] == li-size1 and choose2['Isnum']:
                                    term = FunExg[i['Function_name']](
                                        choose1['Expression'], choose2['Expression'])
                                    # print("计算得term546",term)
                                    Goal = []  # 计算goal
                                    for k1, h in zip(choose1['outputData'], choose2['outputData']):
                                        Goal.append(FunExg[i['Function_name']](k1, h))
                                    if Goal not in SigSet:  # 更新SigSet ExgSet
                                        SigSet.append(Goal)
                                        i['outputData'] = Goal
                                        ExpSet.append({'Expression': term,'Isnum': True, 'arity': i['arity'], 'outputData': Goal, 'size': li})
                                        for actNum in range(len(actions)):
                                            Term = (actNum,term)
                                            if Term not in cover:
                                                coverTemp = []
                                                for num in range(len(pts)):
                                                    pt = pts[num]
                                                    ptOutput = ptsOutput[num]                                
                                                    for output in ptOutput:
                                                        if output[0] ==actNum and Goal[num] == output[1]:
                                                            coverTemp.append(pt)
                                                # 判断cover[term]是否重复了
                                                if coverTemp != []:
                                                    # print("coverTemp:",coverTemp)
                                                    flag = False
                                                    for t in cover:
                                                        if len(cover[t]) == len(coverTemp):
                                                            list1 = deepcopy(cover[t])
                                                            list2 = deepcopy(cover[t])
                                                            if list1.sort() == list2.sort():
                                                                flag = True
                                                                break
                                                    if(flag == False):
                                                        terms.append(Term)
                                                        cover[Term] = coverTemp
                                                        flagHaveTerm = True

            elif  i['Function_name'] == 'Sub': #sub(var,-)
                if li <= 3:
                    for size1 in range(1, li):
                        for choose1 in ExpSet:
                            if choose1['size'] == size1 and choose1['Isnum'] == False:
                                for choose2 in ExpSet:
                                    if choose2['size'] == li-size1:
                                        term = FunExg[i['Function_name']](
                                            choose1['Expression'], choose2['Expression'])
                                        # print("计算得term590",simplify(term))
                                        Goal = []  # 计算goal
                                        for k1, h in zip(choose1['outputData'], choose2['outputData']):
                                            Goal.append(FunExg[i['Function_name']](k1, h))
                                        if Goal not in SigSet:  # 更新SigSet ExgSet
                                            SigSet.append(Goal)
                                            i['outputData'] = Goal
                                            ExpSet.append({'Expression': term,'Isnum': False,'arity': i['arity'], 'outputData': Goal, 'size': li})
                                            for actNum in range(len(actions)):
                                                Term = (actNum,term)
                                                if Term not in cover:
                                                    coverTemp = []
                                                    for num in range(len(pts)):
                                                        pt = pts[num]
                                                        ptOutput = ptsOutput[num]                                
                                                        for output in ptOutput:
                                                            if output[0] ==actNum and Goal[num] == output[1]:
                                                                coverTemp.append(pt)
                                                    # 判断cover[term]是否重复了
                                                    if coverTemp != []:
                                                        # print("coverTemp",coverTemp)
                                                        flag = False
                                                        for t in cover:
                                                            if len(cover[t]) == len(coverTemp):
                                                                list1 = deepcopy(cover[t])
                                                                list2 = deepcopy(cover[t])
                                                                if list1.sort() == list2.sort():
                                                                    flag = True
                                                                    break
                                                        if(flag == False):
                                                            terms.append(Term)
                                                            cover[Term] = coverTemp
                                                            flagHaveTerm = True  
        li += 1                                                                                   
        # termMaxSize += 1
        # print(termMaxSize)
    interResultTerm = InterResult(ExpSet,SigSet)

def nextSizeTerm(termMaxSize,DTFlag):
    #枚举动作的一个参数 返回 [actNum,paraNum,paraTerm]
    print("next size of term:",termMaxSize)
    global interResultTerm
    ExpSet = []  
    SigSet = []
    if  DTFlag:
        sizeOneExps = []
        sizeOneExps.append({'Expression': 0,'Isnum':True, 'arity': 0, 'size': 1})
        sizeOneExps.append({'Expression': 1,'Isnum':True, 'arity': 0, 'size': 1})
        sizeOneExps.append({'Expression': X,'Isnum':False,'arity': 1, 'size': 1})
        if Game["var_num"] == 2:
            sizeOneExps.append({'Expression': X1,'Isnum':False, 'arity': 1, 'size': 1})
        elif Game["var_num"] == 3:
            sizeOneExps.append({'Expression': X1, 'Isnum': False, 'size': 1})
            sizeOneExps.append({'Expression': X2, 'Isnum': False, 'size': 1})
        for i in Game["appeal_constants"]:
            sizeOneExps.append({'Expression': eval(i), 'Isnum': True, 'size': 1})
        for i in sizeOneExps:
            if i['Isnum'] :  # 枚举 0和1 不需要计算出k
                Goal = []
                term = i['Expression']  
                for num in range(len(pts)):
                    Goal.append(i['Expression'])
                if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                    SigSet.append(Goal)
                    i['outputData'] = Goal
                    ExpSet.append(i)
            else:
                if i['Expression'] == X:
                    Goal = []
                    term = X
                    for pt in pts:
                        Goal.append(pt[0])
                    if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                        SigSet.append(Goal)
                        i['outputData'] = Goal
                        ExpSet.append(i)
                if i['Expression'] == X1:
                    Goal = []
                    term = X1
                    for pt in pts:
                        Goal.append(pt[1])
                    if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                        SigSet.append(Goal)
                        i['outputData'] = Goal
                        ExpSet.append(i)
                if i['Expression'] == X2:
                    Goal = []
                    term = X2
                    for pt in pts:
                        Goal.append(pt[2])
                    if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                        SigSet.append(Goal)
                        i['outputData'] = Goal
                        ExpSet.append(i)
    li = 2
    if DTFlag == False:
        SigSet = interResultTerm.SigSet
        ExpSet = interResultTerm.ExpSet
        li = termMaxSize
    while li <= termMaxSize:
        for i in t_vocabulary:
            if i['Function_name'] == 'Add':
                if li <= 3:  #add(var,-)
                    for size1 in range(1, li):
                        for choose1 in ExpSet:
                            if choose1['size'] == size1 and choose1['Isnum'] == False:
                                for choose2 in ExpSet:
                                    if choose2['size'] == li-size1:
                                        term = FunExg[i['Function_name']](
                                            choose1['Expression'], choose2['Expression'])
                                        # print("计算得term505",term)
                                        Goal = []  # 计算goal
                                        for k1, h in zip(choose1['outputData'], choose2['outputData']):
                                            Goal.append(FunExg[i['Function_name']](k1, h))
                                        if Goal not in SigSet:  # 更新SigSet ExgSet
                                            SigSet.append(Goal)
                                            i['outputData'] = Goal
                                            ExpSet.append({'Expression': term, 'Isnum': False,'arity': i['arity'], 
                                                        'outputData': Goal, 'size': li})
                for size1 in range(1,li): #add(num,num)
                    for choose1 in ExpSet:
                        if choose1['size'] == size1 and choose1['Isnum'] :
                            for choose2 in ExpSet:
                                if choose2['size'] == li-size1 and choose2['Isnum']:
                                    term = FunExg[i['Function_name']](
                                        choose1['Expression'], choose2['Expression'])
                                    # print("计算得term546",term)
                                    Goal = []  # 计算goal
                                    for k1, h in zip(choose1['outputData'], choose2['outputData']):
                                        Goal.append(FunExg[i['Function_name']](k1, h))
                                    if Goal not in SigSet:  # 更新SigSet ExgSet
                                        SigSet.append(Goal)
                                        i['outputData'] = Goal
                                        ExpSet.append({'Expression': term,'Isnum': True, 'arity': i['arity'], 'outputData': Goal, 'size': li})
            elif  i['Function_name'] == 'Sub': #sub(var,-)
                if li <= 3:
                    for size1 in range(1, li):
                        for choose1 in ExpSet:
                            if choose1['size'] == size1 and choose1['Isnum'] == False:
                                for choose2 in ExpSet:
                                    if choose2['size'] == li-size1:
                                        term = FunExg[i['Function_name']](
                                            choose1['Expression'], choose2['Expression'])
                                        # print("计算得term590",simplify(term))
                                        Goal = []  # 计算goal
                                        for k1, h in zip(choose1['outputData'], choose2['outputData']):
                                            Goal.append(FunExg[i['Function_name']](k1, h))
                                        if Goal not in SigSet:  # 更新SigSet ExgSet
                                            SigSet.append(Goal)
                                            i['outputData'] = Goal
                                            ExpSet.append({'Expression': term,'Isnum': False,'arity': i['arity'], 'outputData': Goal, 'size': li})                           
        li += 1                                                                                   
    interResultTerm = InterResult(ExpSet,SigSet)
    for actNum in range(len(actions)):
        action = actions[actNum]
        if len(action["action_parameter"])==1:
            for item in ExpSet:
                term = item['Expression']
                Goal = item["outputData"]
                Term = (actNum,term)
                if Term not in cover:
                    coverTemp = []
                    for num in range(len(pts)): #判断所有的点有多少个满足pt
                        pt = pts[num]
                        ptOutput = ptsOutput[num]
                        for output in ptOutput: # 一个input对应多个output
                            if output[0] == actNum and Goal[num] == output[1] and len(output)==2:
                                coverTemp.append(pt)
                                break
                    if coverTemp != []:
                        flag = False
                        for t in cover:
                            if len(cover[t]) == len(coverTemp):
                                list1 = deepcopy(cover[t])
                                list2 = deepcopy(cover[t])
                                if list1.sort() == list2.sort():
                                    flag = True
                                    break
                        if(flag == False):
                            terms.append(Term)
                            cover[Term]=coverTemp
        if len(action["action_parameter"]) == 2:
            for item1 in ExpSet:
                term1 = item1["Expression"]
                Goal1 = item1["outputData"]
                for item2 in ExpSet:
                    term2 = item2["Expression"]
                    Goal2 = item2["outputData"]
                    Term = (actNum,term1,term2)
                    if Term not in cover:
                        coverTemp = []
                        for num in range(len(pts)):
                            pt = pts[num]
                            ptOutput = ptsOutput[num]
                            for output in ptOutput:
                                if len(output)==3 and output[0] == actNum and Goal1[num] == output[1] and Goal2[num] == output[2]:
                                    coverTemp.append(pt)
                                    break
                        if coverTemp != []:
                            flag = False
                            for t in cover:
                                if len(cover[t]) == len(coverTemp):
                                    list1 = deepcopy(cover[t])
                                    list2 = deepcopy(cover[t])
                                    if list1.sort() == list2.sort():
                                        flag = True
                                        break
                            if(flag == False):
                                terms.append(Term)
                                cover[Term]=coverTemp

"""递归合成一颗树"""
def learn_DT(pts, preds):
    # 递归出口，存在一个term满足所有的pt
    if pts == []:  # PTS为空不会生成树，设定一颗默认的树
        return TreeNode(X == X)
    for term in terms:
        if not[False for i in pts if i not in cover[term]]:
            # print("叶子结点：",term)
            return TreeNode(str(term))  # 这里把term设置为了str型
    if preds == [] or preds == None:
        return None
    Pick_pred = chooseBestPred(pts, preds)
    print("Choose best predicate :\n\t", Pick_pred)
    if Pick_pred == False:  # 谓词不足以去划分
        global DTflag  # 全局变量DTflag来检测是否有树生成
        DTflag = False
        global RedundantPts 
        RedundantPts = pts
        return None
    root = TreeNode(Pick_pred)
    ptsYes = []
    ptsNo = []
    for pt in pts:
        if ptSatPred(pt, Pick_pred):
            ptsYes.append(pt)
        else:
            ptsNo.append(pt)
    # print("Divide two part:\n\t")
    # print(ptsYes, ":", ptsNo)
    temp_preds = preds  # 不用深度复制
    temp_preds.remove(Pick_pred)
    # print("剩余的谓词",temp_preds)
    root.left = learn_DT(ptsYes, temp_preds)
    root.right = learn_DT(ptsNo, temp_preds)

    return root

# def Entropy(pts):
#     # print("熵")
#     if len(pts) == 0:
#         return 0
#     entropy = 0.0
#     sumcount = 0
#     for pt in pts:
#         for term in terms:
#             if pt in cover[term]:
#                 sumcount += 1
#     for term in terms:
#         probability = 0.0
#         for pt in pts:
#             if pt not in cover[term]:
#                 probability += 0
#             else:
#                 probability += (1/len(pts))*(count_num_pt(term, pts)/sumcount)
#         # print(term,"计算条件概率是", probability)
#         if probability != 0:
#             entropy -= probability * log(probability, 2)
#     # print("熵为", entropy)
#     return entropy
def Entropy(pts):
    # print("熵")
    if len(pts) == 0:
        return 0
    entropy = 0.0
    # print("概率和是为1吗：")
    for term in terms:
        probability = 0.0
        for pt in pts:
            sumcount = 0
            if pt not in cover[term]:
                probability += 0
            else:
                for term1 in terms:
                    if pt in cover[term1]:
                        sumcount+=1 
                probability += (1/len(pts))*(1/sumcount)
        # print(term,"计算条件概率是", probability)
        if probability != 0:
            entropy -= probability * log(probability, 2)
        # print(term,probability)
    # print("熵为", entropy)
    return entropy


# cover(term)覆盖pts点的个数
def count_num_pt(term, pts):
    count = 0
    for pt in pts:
        if pt in cover[term]:
            count += 1
    return count


def chooseBestPred(pts, preds):  # 返回最大的list
    Best = {'maxInfoGain': 0, 'predicate': False}
    # print("Set of predicates\n\t", preds)
    # print("pts:", pts)
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
        # InfoGain =(len(ptsYes)/len(pts)) * \
        #     Entropy(ptsYes) +(len(ptsNo)/len(pts))*Entropy(ptsNo)
        InfoGain = Entropy(pts)-(len(ptsYes)/len(pts)) * \
            Entropy(ptsYes) - (len(ptsNo)/len(pts))*Entropy(ptsNo)
        # print("信息增益为",InfoGain)
        if InfoGain > Best['maxInfoGain']:
            Best['maxInfoGain'] = InfoGain
            Best['predicate'] = pred
    return Best['predicate']

    # Not(False)


def ptSatPred(pt, pred) -> bool:  # 将pt值代替pred中的未知数
    pred = str(pred)
    # if 'X' in pred:不需要判断，没有得话不会去执行
    if Game["var_num"] == 2:
        pred = pred.replace('X1', str(pt[1]))
    elif Game["var_num"] == 3:
        pred = pred.replace('X1', str(pt[1])).replace('X2', str(pt[2]))
    pred = pred.replace('X', str(pt[0]))
    return eval(pred)


"""生成的树转化成表达式"""


def tree2Expr(DT) -> str:
    if not DT:
        return "False"
    if DT == True:  # 假设的是pts为空 将树默认设置为True
        return "True"
    expr = ""
    # 'NoneType' object has no attribute 'val'
    if(type(DT.val) == type("False")):
        return DT.val
    if (type(DT.val) == type(X == X1)):
        expr = "If("+str(DT.val)+","+tree2Expr(DT.left) + \
            ","+tree2Expr(DT.right)+")"
    if(type(DT.val) == type(X) or type(DT.val) == type(0)):
        expr = str(DT.val)
    return expr


"""将树转化成Z3表达式"""


def tree2LossingFormula(DT) -> str:
    if DT == True:  # 假设的是pts为空 将树默认设置为True
        return "True"
    if(type(DT.val) == type("False")):
        # print(DT.val)
        return DT.val
    t2ftime = time.time()
    paths = []  # 存储一条路径 And(,,,)
    # 如果single大于0 那么就 Or(,,,)起来
    stack = []  # python中栈y用数组实现 存放结点
    p = DT
    pre = None
    while(p != None or len(stack) != 0):
        # 到达最左边 p是非空谓词
        while(p != None and type(p.val) != type("term")):
            stack.append(p)
            p = p.left
        # 此时候p一定是叶子结点
        if p != None and p.val == "True":
            if len(stack) == 1:
                paths.append(stack[0].val)
            else:
                expr = "And("
                for i in stack:
                    expr = expr+str(i.val)+","
                expr = expr[0:len(expr)-1]+")"
                paths.append(expr)
        p = stack.pop()  # p.left是term
        # 如果是叶子结点 且非访问过
        if(type(p.right.val) == type("term") or p.right == pre):
            if(type(p.right.val) == type("term") and p.right.val == "True"):
                p.val = Not(p.val)
                stack.append(p)
                if len(stack) == 1:
                    paths.append(stack[0].val)
                else:
                    expr = "And("
                    for i in stack:
                        # print(i.val)
                        expr = expr+str(i.val)+","
                    expr = expr[0:len(expr)-1]+")"
                    paths.append(expr)
                stack = stack[:-1]
            pre = p
            p = None
        else:
            # 非叶子结点
            p.val = Not(p.val)
            stack.append(p)
            p = p.right
    if len(paths) == 1:
        # print("Tiem of tree transform normal expression：", time.time()-t2ftime)
        return str(paths[0])
    else:
        expr = "Or("
        for i in paths:
            expr = expr+str(i)+","
        # 会多出一个逗号
        expr = expr[0:len(expr)-1]+")"
        # print("Time of tree transform normal expression：", time.time()-t2ftime)
        return expr


"""global transition formula"""
global_transition_formula = "Or("
for i in Game["actions"]:
    if i['action_parameter'] != []:
        temp = "["
        for j in i['action_parameter']:
            temp = temp+str(j)+","
        temp = temp[:-1]
        temp += "],"
        global_transition_formula = global_transition_formula + \
            "Exists("+temp+str(i["transition_formula"])+"),"
    else:
        global_transition_formula = global_transition_formula + \
            str(i["transition_formula"])+","

global_transition_formula = global_transition_formula[:-1]
global_transition_formula = global_transition_formula+")"

print("Global transition formula:\n\t", global_transition_formula)
global_transition_formula = simplify(eval(global_transition_formula))

"""
递归得到反例所要使用的点集合
"""
position = []
if Game['var_num'] == 1:
    for i in range(0, 100):
        position.append('illegal')
elif Game['var_num'] == 2:
    for i in range(0, 100):
        position.append([])
        for j in range(0, 100):
            position[i].append('illegal')
elif Game['var_num'] == 3:
    for i in range(0, 100):
        position.append([])
        for i1 in range(0, 100):
            position[i].append([])
            for i2 in range(0, 100):
                position[i][i1].append("illegal")

"""
set all terminate state position  #求出范围内所有的终态位置 一般是一个，但有时不止一个
"""
TerminatePosition = []  # 保存已经求出来的解点坐标
while(True):
    s = Solver()
    s.add(Game["Terminal_Condition"])
    s.add(Game["Constraint"])
    if Game["var_num"] == 1:
        s.add(X < 100)
        for i in TerminatePosition:
            s.add(X != i)
        if(s.check() == sat):
            m = s.model()
            a = m[X].as_long()
            TerminatePosition.append(a)
            if Game["type"] == "normal":
                position[a] = True  # normal
            else:
                position[a] = False  # misere
        else:
            break
    elif Game["var_num"] == 2:
        s.add(X < 100, X1 < 100)
        for i in TerminatePosition:
            s.add(Or(X != i[0], X1 != i[1]))
        if s.check() == sat:
            m = s.model()
            a = m[X].as_long()
            b = m[X1].as_long()
            TerminatePosition.append([a, b])
            if(Game["type"] == "normal"):
                position[a][b] = True
            else:
                position[a][b] = False
        else:
            break
    elif Game["var_num"] == 3:
        s.add(X < 100, X1 < 100, X2 < 100)
        for i in TerminatePosition:
            s.add(Or(X != i[0], X1 != i[1], X2 != i[2]))
        if s.check() == sat:
            m = s.model()
            a = m[X].as_long()
            b = m[X1].as_long()
            c = m[X2].as_long()
            TerminatePosition.append([a, b, c])
            if(Game["type"] == "normal"):
                position[a][b][c] = True
            else:
                position[a][b][c] = False
        else:
            break
print("All terminate position:\n\t", TerminatePosition)


# v is a position,judge it is a lossing_state

# Or(Exists([k1,k2,k3],And(And(X > 3, k1 > 0, k2 > 0, k3 > 0),And(Y == k1, Y1 == k2, Y2 == k3))),
#     Exists([k1,k2,k3],And(And(X1 > 3, k1 > 0, k2 > 0, k3 > 0),And(Y == k1, Y1 == k2, Y2 == k3))),
#     Exists([k1,k2,k3],And(And(X2 > 3, k1 > 0, k2 > 0, k3 > 0),And(Y == k1, Y1 == k2, Y2 == k3))))
def isLossingState(*v):
    # print("Insert",v," into isLossingstate:")
    for i in v:  # default position < 100
        if i >= 100:
            return 'illegal'
    if len(v) == 1:
        if position[v[0]] != 'illegal':
            return position[v[0]]
        for x in range(0, v[0] + 1):
            if (position[x] != 'illegal'):
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
                if (position[i[0]] == 'illegal'):
                    position[i[0]] = isLossingState(i[0])
            for i in temp:
                is_losing = is_losing and not position[i[0]]
            if (is_losing):
                position[x] = True
            else:
                position[x] = False
        return position[v[0]]
    elif len(v) == 2:
        if position[v[0]][v[1]] != 'illegal':  # 已经访问过了的，直接访问值，没有的
            return position[v[0]][v[1]]
        for x in range(0, v[0]+1):  # 遍历所有的点去设置状态
            for y in range(0, v[1]+1):
                if(position[x][y] != 'illegal'):
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
                # print('Transilate 773 of',x,y,":\t",temp) #存放状态 438 [[2, 1], [2, 0], [1, 1]]
                is_losing = True
                s = Solver()
                s.add(Game["Constraint"])
                s.add(X == x, X1 == y)
                if(s.check() == unsat):
                    continue
                for i in temp:
                    if(position[i[0]][i[1]] == 'illegal'):
                        position[i[0]][i[1]] = isLossingState(i[0], i[1])
                for i in temp:
                    is_losing = is_losing and not position[i[0]][i[1]]
                if (is_losing):
                    position[x][y] = True
                else:
                    position[x][y] = False
        # print("判断出给定的表达式：",v,"is",position[v[0]][v[1]])
        return position[v[0]][v[1]]
    elif len(v) == 3:
        if position[v[0]][v[1]][v[2]] != 'illegal':  # 已经访问过了的，直接访问值，没有的
            return position[v[0]][v[1]][v[2]]
        for x in range(0, v[0]+1):  # 遍历所有的点去设置状态
            for y in range(0, v[1]+1):
                for z in range(0, v[2]+1):
                    if(position[x][y][z] != 'illegal'):
                        continue
                    temp = []  # 存放转移后的解 y y1即执行动作后的值
                    while (True):
                        s = Solver()
                        s.add(global_transition_formula)
                        s.add(Game["Constraint"])
                        s.add(X == x, X1 == y, X2 == z)
                        for i in temp:
                            s.add(Or(Y != i[0], Y1 != i[1], Y2 != i[2]))
                        if s.check() == sat:
                            m = s.model()
                            temp.append(
                                [m[Y].as_long(), m[Y1].as_long(), m[Y2].as_long()])  # 全局转移解
                        else:
                            break
                    # print('438',temp) 存放状态 438 [[2, 1], [2, 0], [1, 1]]
                    is_losing = True
                    s = Solver()
                    s.add(Game["Constraint"])
                    s.add(X == x, X1 == y, X2 == z)
                    if(s.check() == unsat):
                        continue
                    for i in temp:
                        if(position[i[0]][i[1]][i[2]] == 'illegal'):
                            position[i[0]][i[1]][i[2]] = isLossingState(
                                i[0], i[1], i[2])
                    for i in temp:
                        is_losing = is_losing and not position[i[0]
                                                               ][i[1]][i[2]]
                    if (is_losing):
                        position[x][y][z] = True
                    else:
                        position[x][y][z] = False
        return position[v[0]][v[1]][v[2]]


# 宽松反例---遍历一个满足约束不在反例集中的点 ptList=[[pt1],[pt2],[pt3]]
def FindCountExample(ptList):
    if Game["var_num"] == 1:
        i = 1
        while(True):
            if i>100:
                global example_run_out_sign 
                example_run_out_sign = True
                return 'illegal'
            for v1 in range(0, i):
                if [v1] not in ptList and [v1] not in pts:
                    s = Solver()
                    s.add(Game["Constraint"])
                    s.add(X == v1)
                    if (s.check() == sat):
                        return [v1]
                        # 严格反例模式
                        boolTemp = isLossingState(v1)
                        boolTemp2 = eval(str(e).replace(
                            str(X), str(v1)))
                        s = Solver()
                        if boolTemp == False:
                            s.add(True, boolTemp2)
                            if(s.check() == sat):
                                return [v1]
                        elif boolTemp == True:
                            s.add(True, boolTemp2)
                            if(s.check() == unsat):
                                return [v1]
                    else:
                        continue
            i += 1
    elif Game["var_num"] == 2:
        i = 1
        if i>100:
            example_run_out_sign = True
            return 'illegal'
        while(True):
            for v1 in range(0, i+1):  # 没有点（0,1）啊
                v2 = i-v1  # 遍历所有的v1v2=i的组合 按照size遍历
                # print("828",v1,v2)
                if [v1, v2] not in ptList and [v1, v2] not in pts:
                    s = Solver()
                    s.add(Game["Constraint"])  # 满足约束条件
                    s.add(X == v1, X1 == v2)
                    if s.check() == sat:
                        # print("find example:", v1, v2)
                        return [v1, v2]
                        # print(expr)
                        # 要求在这里就设置为严格反例
                        # print("该轮枚举：", v1, v2)
                        boolTemp = isLossingState(v1, v2)
                        boolTemp2 = eval(str(e).replace(
                            str(X1), str(v2)).replace(str(X), str(v1)))
                        s = Solver()
                        if boolTemp == False:
                            s.add(True, boolTemp2)
                            if(s.check() == sat):
                                return [v1, v2]
                        elif boolTemp == True:
                            s.add(True, boolTemp2)
                            if(s.check() == unsat):
                                return [v1, v2]
                    else:
                        continue
            i = i+1
    elif Game["var_num"] == 3:
        i = 1
        while True:
            if i>100:
                example_run_out_sign = True
                return 'illegal'
            for v1 in range(0, i+1):
                for v2 in range(0, i-v1+1):
                    v3 = i-v1-v2
                    if [v1, v2, v3] not in ptList and [v1, v2, v3]not in pts:
                        s = Solver()
                        s.add(Game["Constraint"])  # 满足约束条件
                        s.add(X == v1, X1 == v2, X2 == v3)
                        if s.check() == sat:
                            return [v1, v2, v3]
                            # 严格反例模式
                            boolTemp = isLossingState(v1, v2, v3)
                            boolTemp2 = eval(str(e).replace(
                                str(X1), str(v2)).replace(str(X2), str(v3)).replace(str(X), str(v1)))
                            s = Solver()
                            if boolTemp == False:
                                s.add(True, boolTemp2)
                                if(s.check() == sat):
                                    return [v1, v2, v3]
                            elif boolTemp == True:
                                s.add(True, boolTemp2)
                                if(s.check() == unsat):
                                    return [v1, v2, v3]
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

# sat 时寻找pt


def outRange(*v):
    for i in v:  # default position < 100
        if i >= 100:
            return 'illegal'

def satfindstate(ptk):
    ptK = ptk
    ptList = []
    m = s.model()
    value = []
    for i in Game["varList"]:
        value.append(m[i].as_long())
    if outRange(*value) != 'illegal':
        ptK -= 1
        ptList.append(value)
        if(ptK == 0):
            return ptList
    while True:
        pt = FindCountExample(ptList)
        if pt =='illegal':#例子用完了，返回ptList
            return ptList
        if outRange(*pt) == 'illegal':
            continue
        else:
            ptK -= 1
            ptList.append(pt)
            if(ptK == 0):
                print( ptk,"example generate:\t", ptList)
                return ptList

def unkownfindstate(ptk):
    ptK = ptk
    ptList = []
    while True:
        pt = FindCountExample(ptList)
        if pt =='illegal':#例子用完了，返回ptList
            return ptList
        if outRange(*pt) == 'illegal':
            continue
        else:
            ptK -= 1
            ptList.append(pt)
            if(ptK == 0):
                print(ptk,"example generate:\t", ptList)
                return ptList


start_winning_formula_time = time.time()
# 合成必败公式
termination_sign = False #超时标志
example_run_out_sign = False #范围内的例子用尽 


def programTimeOut():
    global termination_sign
    termination_sign = True

Thread1 = threading.Timer(3600, programTimeOut)
Thread1.start()
# 将终态添加到反例中
pts = []
ptsGoal = []
# for i in TerminatePosition:
#     pts.append(i)
#     ptsGoal.append(True)


Maxsize = 1
preds = []
while(True):
    if termination_sign or example_run_out_sign:
        print("Time out,about to exit the program")
        Thread1.cancel()
        # write into .xls
        newwb = copy(oldwb)
        sheet1 = newwb.get_sheet(0)
        sheet1.write(row, 0, pddlFile.split('\\')[-1])
        if termination_sign:
            sheet1.write(row, 2, "time-out-1200s")
        if example_run_out_sign:
            sheet1.write(row, 2, "example-run-out,cannot solve")
        newwb.save(resultFile)
        # write into .txt
        # fp = open(resultFile, 'a')
        # fp.write(pddlFile.split('\\')[-1]+"\t")
        # fp.write("time-more-than-600s\n")
        break
    terms = [True, False]
    cover = {}
    cover[True] = []
    cover[False] = []
    for num in range(len(pts)):
        cover[ptsGoal[num]].append(pts[num])
    print("Cover set: \t", cover)
    DT = None
    e = X == X  # 默认表达式
    last_e = e
    DTTime = time.time()
    # CycleNum = 2
    global DTflag
    DTflag = True
    while pts != [] and (DT == None or DTflag == False):
        enumPredsTime = time.time()
        enumeratePredicate(Maxsize,DTflag) #DTflag 表示pred不足接着上次的地方继续枚举谓词
        print("preds:",preds)
        print("Num of pts:  ", len(pts))
        calculateIGTime = time.time()
        DTflag = True
        DT = learn_DT(pts, preds)  # lenrnDT中可能会出现 找出不了最好的谓词划分
        # print("Information gain time ：",time.time()-calculateIGTime)
        if(DTflag == False):
            Maxsize += 1
            # CycleNum -= 1
            # print("剩余循环次数：",CycleNum)
            print('cannot solve,need more predicates,increase Maxsize', Maxsize)
    print("Time of learn DT：", time.time()-DTTime)
    if DT != None:
        e = eval(tree2Expr(DT))
    print("Dicision tree:\n\t", e)
    e1 = eval(str(e).replace("X1", "Y1").replace("X2", "Y2").replace("X", "Y"))
    print("Add expression to verity:\n", e)
    if str(e) != str(last_e):
        if Game["type"] == "normal" :
            con1 = And(Game["Terminal_Condition"], Not(e))
            con2 = And(Game["Constraint"], Not(e), ForAll(
                varListY, Or(Not(global_transition_formula), Not(e1))))
            con3 = And(Game["Constraint"], e, Exists(
                varListY, And(global_transition_formula, e1)))
        else:
            con1 = And(Game["Terminal_Condition"], e)
            con2 = And(Game["Constraint"], Not(e), Not(Game["Terminal_Condition"]), ForAll(
                varListY, Or(Not(global_transition_formula), Not(e1))))
            con3 = And(Game["Constraint"], e, Exists(
                varListY, And(global_transition_formula, e1)))
        s = Solver()
        s.set('timeout', 30000)
        s.add(con1)
        check1 = s.check()
        print(check1)
        if check1 == sat:
            print("unsat con1")
            examples = satfindstate(ptk)
        else:#如果超过100s判断不出是sat就算做是unsat
            print("sat con1")
            s = Solver()
            s.set('timeout', 60000)
            s.add(con2)
            if s.check() == sat:
                print("unsat con2")
                examples = satfindstate(ptk)
            else:
                print("sat con2")
                s = Solver()
                s.set('timeout', 60000)
                s.add(con3)
                if s.check() == sat:
                    print("unsat con3")
                    examples = satfindstate(ptk)
                else:
                    print("sat con3")
                    # losing_formula = e
                    # print("树的表达式：",tree2LossingFormula(DT))
                    resultDT = deepcopy(DT)
                    losing_formula = eval(tree2LossingFormula(DT))
                    print("Loosing formula：", losing_formula)
                    losing_formula_Y = e1
                    winning_formula = simplify(Not(losing_formula))
                    print("-----------------------------")
                    winning_formula_time = time.time()-start_winning_formula_time
                    print("Winning Fromula：", winning_formula)
                    print("Total time：", winning_formula_time)
                    winning_formula_time = str(round(winning_formula_time, 2))

                    newwb = copy(oldwb)
                    sheet1 = newwb.get_sheet(0)
                    sheet1.write(row, 0, pddlFile.split('\\')[-1][:-5])
                    sheet1.write(row, 1, str(winning_formula))
                    sheet1.write(row, 2, winning_formula_time)
                    # newwb.save(resultFile)

                    # fp = open(resultFile, 'a')
                    # fp.write(pddlFile.split('\\')[-1]+"\t")
                    # fp.write(str(simplify(Not(losing_formula))) +
                    #          "\t"+winning_formula_time+"\n")
                    Thread1.cancel()  # 取消计时线程
                    break
    else:
        print("repeat expression")
        examples = unkownfindstate(ptk)
    if Game["var_num"] == 1:
        for i in examples:  # k个反例 [[0],[1],[2]]
            if i[0] not in pts:
                pts.append([i[0]])
                ptsGoal.append(isLossingState(i[0]))
    elif Game["var_num"] == 2:
        for i in examples:
            if [i[0], i[1]] not in pts:
                pts.append([i[0], i[1]])
                ptsGoal.append(isLossingState(i[0], i[1]))
    elif Game["var_num"] == 3:
        for i in examples:
            if [i[0], i[1], i[2]] not in pts:
                pts.append([i[0], i[1], i[2]])
                ptsGoal.append(isLossingState(i[0], i[1], i[2]))
print("=======================================================================")
# print(winning_formula)
winning_formula_Y = eval(str(winning_formula).replace("X1", "Y1")
                    .replace("X2", "Y2").replace("X", "Y"))
# print(losing_formula)
losing_formula_Y = eval(str(losing_formula).replace("X1", "Y1")
                    .replace("X2", "Y2").replace("X", "Y"))
# print(winning_formula_Y)
print("losing_formula_Y:",losing_formula_Y)

# print(actions)
# print(actions[0]['action_name'])
# [{'action_name': 'eat1', 'action_parameter': [k], 'precondition': 
# And(X >= k, k > 1), 'transition_formula': And(And(X >= k, k > 1),
#     And(Y == -1 + k, If(X1 >= k, Y1 == -1 + k, Y1 == X1)))}]
lenActs = len(actions)

def genOutput(pt):
    print("generate outputs of pt",pt)
    outputList=[]
    for i in range(0,lenActs):
        action = actions[i]
        while True:
            s = Solver()
            for output in outputList: #output可能有不同的长度 （0,1） （1,2,3）
                parasLen = len(action["action_parameter"])
                if i == output[0] and parasLen == len(output)-1 :
                    if parasLen == 1: #只有一个参数
                        s.add(k!=output[1])
                    else:
                        con = "Or("
                        for num in range(0,parasLen):
                            con = con + str(action["action_parameter"][num])+"!="+str(output[num+1])+","
                        con = con[:-1]
                        con = con+")"
                        print("1465con:",con)
                        s.add(eval(con))
            if Game['var_num'] == 1:
                s.add(X == pt[0])
            elif Game["var_num"] == 2:
                s.add(X == pt[0],X1 == pt[1])
            elif Game["var_num"] == 3:
                s.add(X == pt[0], X1 == pt[1], X2 == pt[2])
            s.add(actions[i]['precondition'])
            s.add(actions[i]['transition_formula'])
            s.add(losing_formula_Y)
            if s.check() == sat:
                m=s.model()
                ans = [i]
                for para in action["action_parameter"]:
                    ans.append(m[para].as_long()) #addk
                print("exist concrete  action [act,para] ",ans)
                outputList.append(ans)
            else:
                break
    return outputList

#生成的例子满足path（f） game.condition 不满足terCon 
#ptList 每轮生成的例子集合
def genPtSatFormula(formula,ptList):
    if Game['var_num'] == 1:
        i = 1
        while True:
            for v1 in range(0,i+1):
                if [v1] not in ptList and [v1] not in pts:
                    s = Solver()
                    s.add(Game['Constraint']) #满足游戏约束
                    # s.add(Not(Game["Terminal_Condition"])) #不属于终点
                    # s.add(winning_formula)
                    s.add(formula) #满足路径公式
                    s.add(X == v1)
                    if s.check() == sat:
                        print("find state:",v1)
                        return [v1]
            i=i+1
    elif Game['var_num'] == 2:
        i = 1
        while True:
            for v1 in range(0,i+1):
                v2 = i-v1
                if [v1,v2] not in ptList and [v1,v2] not in pts:
                    s = Solver()
                    s.add(Game['Constraint']) #满足游戏约束
                    # s.add(Not(Game["Terminal_Condition"])) #不属于终点
                    # s.add(winning_formula)
                    s.add(formula) #满足路径公式
                    s.add(X == v1, X1 == v2)
                    if s.check() == sat:
                        # print("find state:",v1,v2)
                        return [v1,v2]
            i=i+1
    elif Game['var_num'] == 3:
        i = 1
        while True:
            for v1 in range(0,i+1):
                for v2 in range(0,i-v1+1):
                    v3 = i-v1-v2
                    if [v1,v2,v3] not in ptList and [v1,v2,v3] not in pts:
                        s = Solver()
                        s.add(Game['Constraint']) #满足游戏约束
                        # s.add(Not(Game["Terminal_Condition"])) #不属于终点
                        # s.add(winning_formula)
                        s.add(formula) #满足路径公式
                        s.add(X == v1, X1 == v2, X2 == v3)
                        if s.check() == sat:
                            print("find state:",v1,v2,v3)
                            return [v1,v2,v3]
            i=i+1
    
#返回存放path()的  [str,str...]
def pathOfWF(DT):
    paths =[]
    stack = []
    p = DT
    pre = None #利用双指针实现遍历
    while p!=None or len(stack)!=0 :
        while(p != None and type(p.val) != type("term")):
            stack.append(p)
            p = p.left
        if p != None and p.val == "False":
            if len(stack) == 1:
                paths.append(str(stack[0].val))
            else:
                expr = "And("
                for i in stack:
                    expr = expr+str(i.val)+","
                expr = expr[0:len(expr)-1]+")"
                paths.append(expr)
        p = stack.pop()  # p.left是term
        # 如果是叶子结点 且非访问过
        if(type(p.right.val) == type("term") or p.right == pre):
            if(type(p.right.val) == type("term") and p.right.val == "False"):
                p.val = Not(p.val)
                stack.append(p)
                if len(stack) == 1:
                    paths.append(str(stack[0].val))
                else:
                    expr = "And("
                    for i in stack:
                        # print(i.val)
                        expr = expr+str(i.val)+","
                    expr = expr[0:len(expr)-1]+")"
                    paths.append(expr)
                stack = stack[:-1]
            pre = p
            p = None
        else:
            # 非叶子结点
            p.val = Not(p.val)
            stack.append(p)
            p = p.right
    return paths
print("Decision tree2:",tree2Expr(resultDT))
#所有的路径 list
def pathOfAct(DT):
    if type(DT.val) == type("term"): #只有一个而叶子节点的树
        return  [["",eval(DT.val)]]
    paths =[]
    stack = []
    p = DT
    pre = None #利用双指针实现遍历
    while p!=None or len(stack)!=0 :
        while(p != None and type(p.val) != type("str")):
            stack.append(p)
            p = p.left
        if p != None :
            if len(stack) == 1:
                paths.append([stack[0].val,eval(p.val)])
            else:
                expr = "And("
                for i in stack:
                    expr = expr+str(i.val)+","
                expr = expr[0:len(expr)-1]+")"
                paths.append([eval(expr),eval(p.val)])
        p = stack.pop()  # p.left是term
        # 如果是叶子结点 且非访问过
        if(type(p.right.val) == type("term") or p.right == pre):
            if type(p.right.val) == type("term") :
                p.val = Not(p.val)
                stack.append(p)
                if len(stack) == 1:
                    paths.append([stack[0].val,eval(p.right.val)])
                else:
                    expr = "And("
                    for i in stack:
                        # print(i.val)
                        expr = expr+str(i.val)+","
                    expr = expr[0:len(expr)-1]+")"
                    paths.append([eval(expr),eval(p.right.val)])
                stack = stack[:-1]
            pre = p
            p = None
        else:
            # 非叶子结点
            p.val = Not(p.val)
            stack.append(p)
            p = p.right
    return paths
#THIS term = [act.id parameter]
def isTermSatExample(term,pt,output):
    if output[0] != term[0] and len(output)!= len(term):
        return False
    if Game["var_num"] == 2:
        for i in range(1,len(term)):#term [0,X], [0,X,Y] 每个参数都比较
            if eval(str(term[i]).replace('X1',str(pt[1])).replace('X',str(pt[0]))) != output[i]:
                return False
        return True
    elif Game['var_num'] == 3: #[0,5,1] [0,X-X2,X1-X2]
        for i in range(1,len(term)):
            if eval(str(term[i]).replace('X1',str(pt[1])).replace('X2',str(pt[2])).replace('X',str(pt[0]))) != output[i]:
                return False
        return True
    elif Game["var_num"] == 1:
        for i in range(1,len(term)):
            if eval(str(term[i]).replace('X',str(pt[0]))) != output[i]:
                return False
        return True
# Ensure that pt-outputs all output have term cover
#每个out都要有至少一个term cover
def ptsAllCover():
    print("++++++++++ each pt have term cover ++++++++++++++")
    for num in range(len(pts)):
        pt = pts[num]
        ptOutput = ptsOutput[num] #一个点对应多个ptoutput 
        for output in ptOutput:
            flag_cover = False
            for term in terms:
                if isTermSatExample(term,pt,output):
                    flag_cover = True
                    break
            if flag_cover == False :# 需要枚举出cover来满足ptGoal[1] 
                print(pt,"not term cover,ptoutput:",)
                if len(output) == 2:
                    term=(output[0],enumerateTerm(pt,output[1]))
                elif len(output) == 3:
                    term=(output[0],enumerateTerm(pt,output[1]),enumerateTerm(pt,output[2])) 
                elif len(output) == 4:
                    term=(output[0],enumerateTerm(pt,output[1]),enumerateTerm(pt,output[2]),enumerateTerm(pt,output[3]))
                print("find term",term,"cover")
                if term not in cover:
                    terms.append(term)
                    cover[term] = []
                cover[term].append(pt)
#更新所有的terms，pts的关系
def updateCover():
    print("update caver.........")
    for term in terms:
        for num in range(0,len(pts)):
            pt = pts[num]
            ptOutput = ptsOutput[num]
            if pt not in cover[term]:
                for output in ptOutput:
                    if isTermSatExample(term,pt,output):
                        cover[term].append(pt)
                        break

"""将树转化为必胜策略公式 叶子节点--动作"""
def tree2WinningStrategy(DT) ->str:
    expr = ""
    if type(DT.val) == type("str"):
        term = eval(DT.val)
        action = actions[term[0]]
        action = eval(str(action).replace("k", '('+str(term[1])+')'))
        return str(action["transition_formula"])
    if (type(DT.val) == type(X == X1)):
        expr = "If("+str(DT.val)+","+tree2WinningStrategy(DT.left) +","+tree2WinningStrategy(DT.right)+")"
    return expr        

def tree2Act(DT):
    if DT == None : return "None"
    expr = ""
    if type(DT.val) == type("term"):
        term = eval(DT.val)
        action = actions[term[0]]
        return str(action["action_name"])+"("+ str(term)[4:]
    if (type(DT.val) == type(X == X1)):
        expr = "If("+str(DT.val)+","+tree2Act(DT.left) +","+tree2Act(DT.right)+")"
    return expr 

def defaultAction():
    S1 = Solver()
    S1.add(Game["Constraint"])
    S1.add(Game["actions"][0]["precondition"])
    if S1.check() == sat:
        m=S1.model()
        para = m[k].as_long()
        return [["",(0,para)]]
    return

def defaultPreds(pathFormula):
    str1 = str(pathFormula)
    str1 = str1.replace(' ', '').replace("\n","")
    arr1 = [] 
    if "And" in str1:     # And(f1, f2, f3 ,f4)
        str1 = str1[4:-1]
        arr = str1.split(",")
    else:                 # f1
        arr = [str1]
    for s in arr:
        if "Not" in s: 
            s = s[4:-1]
            if "%" in s: # a%b==c
                b = s[s.find('%')+1:s.find("==")]
                c = s[s.find("==")+2:]
                for i in range(0,eval(b)):
                    if  str(i) != c:
                        arr1.append(s[:s.find("==")+2]+str(i))
            elif "==" in s: #==
                arr1.append(s.replace("==",">"))
                arr1.append(s.replace("==","<"))
        else:
            if ">=" in s:
                arr1.append(s.replace(">=",">"))
                arr1.append(s.replace(">=","=="))
            elif "<=" in s:
                arr1.append(s.replace("<=","<"))
                arr1.append(s.replace("<=","=="))          
    preds = []
    for i in arr1:
        i = eval(i)
        preds.append(i)
    return preds

def isPtSatForm(pt,form):
    s1 = Solver()
    s1.add(form)
    if Game['var_num'] == 1:
        s1.add(X == pt[0])
        if s1.check()==sat:
            return True
        else:
            return False
    elif Game['var_num'] == 2:
        s1.add(X == pt[0],X1== pt[1])
        if s1.check()==sat:
            return True
        else:
            return False
    elif Game['var_num'] == 3:
        s1.add(X == pt[0],X1== pt[1],X2 ==pt[2])
        if s1.check()==sat:
            return True
        else:
            return False
    
def refinementPath(pathFormula):
    ans = [] #一个或多个 
    str1 = str(pathFormula)
    str1 = str1.replace(' ', '').replace("\n","")
    arr1 = []
    if "And" in str1:
        str2 = str1[str1.rfind(",")+1:-1]
    else:
        str2 = str1
    if "Not" in str2: 
        str2 = str2[4:-1]
        if "%" in str2: # a%b==c
            b = str2[str2.find('%')+1:str2.find("==")]
            c = str2[str2.find("==")+2:]
            for i in range(0,eval(b)):
                if  str(i) != c:
                    arr1.append(str2[:str2.find("==")+2]+str(i))
        elif "==" in str2: #==
            arr1.append(str2.replace("==",">"))
            arr1.append(str2.replace("==","<"))
    else:
        if ">=" in str2:
            arr1.append(str2.replace(">=",">"))
            arr1.append(str2.replace(">=","=="))
        elif "<=" in str2:
            arr1.append(str2.replace("<=","<"))
            arr1.append(str2.replace("<=","==")) 
    if arr1 == []:
        arr1.append(str2)
    for f in arr1:
        if "And" in str1:
            ans.append(str1.replace(str1[str1.rfind(",")+1:],f)+")")
        else:
            ans.append(f)
    # print("refinement path :",ans)
    return ans




ptsOld = cover[False]


print("winning formula used pts:",ptsOld)
print(eval(tree2Expr(DT)))
print("Decision tree1:",tree2Expr(resultDT))
formulaPaths = pathOfWF(deepcopy(resultDT))
print("All paths: ",formulaPaths)


termination_sign = False #超时标志
time_out2 = 3600
Thread2 = threading.Timer(time_out2, programTimeOut)
Thread2.start()

startWinningStrategyTime = time.time()
winningStrategy = []
refineFormulaPaths = []
for pathFormula in formulaPaths:
    for f in refinementPath(pathFormula):
        s = Solver()
        s.add(eval(f))
        s.add(Game['Constraint'])
        if s.check()==sat:
            refineFormulaPaths.append(f)
print("refine formula path:\n",refineFormulaPaths)
exitFlag = False
for pathFormula in refineFormulaPaths:
    if exitFlag: break #跳出多重循环
    print("############### one path:",pathFormula,"#################")
    pathFormula = eval(pathFormula) #str --> z3 
    pts = []
    for pt in ptsOld:
        if isPtSatForm(pt,pathFormula):
            pts.append(pt)
    ptsOutput = []
    for pt in pts: #例子 pt[state]-output【act k 】
        outputs = genOutput(pt)
        ptsOutput.append(outputs)
    preds = defaultPreds(pathFormula)
    print("defaultPreds:\n",preds)
    terms = []
    cover = {}
    maxSizePred = 1
    maxSizeTerm = 0
    while True:
        """超时设置"""
        if termination_sign:
            print("Time out,about to exit the program")
            Thread2.cancel()
            sheet1.write(row,3,"time-out-"+str(time_out2))
            newwb.save(resultFile)
            exitFlag = True
            break
        print("pts",pts)
        ptsAllCover()
        updateCover()
        for key,val in cover.items():
            print(key,":",val)
        # cycleNum = 2
        DTflag = True
        DT = None
        # while cycleNum != 0 and pts !=[] and (DT == None or DTflag == False):
        while pts !=[] and (DT == None or DTflag == False):
            maxSizeTerm += 1
            nextSizeTerm(maxSizeTerm,DTflag)
            print("terms\n",terms)
            enumeratePredicate(maxSizePred,DTflag)
            updateCover()
            print("preds\n",preds)
            print("pts\n",pts)
            print("ptsOutput\n",ptsOutput)
            print("cover:")
            for key,val in cover.items():
                print(key,":",val)
            DTflag = True
            DT = learn_DT(pts,preds)  
            if DTflag == False:
                # print("cannot divide pts",RedundantPts)
                maxSizePred += 1
                # cycleNum -= 1
                DT =None
                # print("剩余的循环次数：",cycleNum)
                print('cannot solve,need more predicates maxszie:',maxSizePred," and more term")
        print("candidate tree",tree2Act(DT))
        # pathWinningStrategy = eval(tree2WinningStrategy(DT))
        """"  vertify  """
        # ActPaths = defaultAction() #默认动作
        if DT != None:
            ActPaths = pathOfAct(DT) 
            print("Path:",pathFormula,"All canditate streaty:",ActPaths)#[[X2 == 1, (0, 1, 1)]]
            isSAT = True
            winningStrategyTemp = []
            for path in ActPaths:
                concreteAct = path[1]  #(0,1,1)
                action = actions[concreteAct[0]]
                ActExe = action['action_name']+'('+ str(concreteAct)[4:]
                for i  in range(1,len(concreteAct)): #k值赋值要用括号包着,k1,k2,k3
                    action = eval(str(action).replace(str(action["action_parameter"][i-1]),"("+str(concreteAct[i])+")"))
                preAct = action["precondition"]
                transitionFormula = action["transition_formula"]
                if type(path[0]) !=type(""):
                    winningStrategyPath = And(pathFormula,path[0])
                    con = Not(Implies(And(Game["Constraint"],pathFormula,path[0]),
                        And(preAct,ForAll(varListY,Implies(transitionFormula,losing_formula_Y)))))
                else:
                    winningStrategyPath = pathFormula
                    con = Not(Implies(And(Game["Constraint"],pathFormula),
                        And(preAct,ForAll(varListY,Implies(transitionFormula,losing_formula_Y)))))
                print("Test this path:\n",winningStrategyPath,"execute action:",ActExe)

                s = Solver()
                s.set('timeout', 60000)
                s.add(con)
                if s.check() == sat:
                    print("==========generate example========")
                    ptK = ptk2 
                    ptList = []
                    value = []
                    m = s.model()
                    for i in Game['varList']:
                        value.append(m[i].as_long())
                    print("策略不满足,反例是:",value)
                    ptK = ptK - 1
                    ptList.append(value) 
                    # while ptK>0:
                    #     if len(value) == 1:
                    #         s.add(X!=value[0])
                    #     elif len(value) == 2:
                    #         s.add(Or(X!=value[0],X1!=value[1]))
                    #     elif len(value) ==3:
                    #         s.add(Or(X!=value[0],X1!=value[1],X2!=value[2]))
                    #     if s.check() == sat:
                    #         m = s.model()
                    #         value =[]
                    #         for i in Game['varList']:
                    #             value.append(m[i].as_long())  
                    #         print("策略不满足,反例是:",value)
                    #         ptK = ptK - 1
                    #         ptList.append(value)         

                    while ptK>0:#不严格的找出反例
                        pt = genPtSatFormula(pathFormula,ptList)
                        ptList.append(pt)
                        ptK = ptK - 1
                    print(ptk2," example have generate:",ptList)
                    for pt in ptList:
                        pts.append(pt)
                        ptsOutput.append(genOutput(pt))
                    isSAT = False
                    print("====================================")
                    break
                else:
                    winningStrategyTemp.append([winningStrategyPath,ActExe])
                    print(path,"sat...")
        elif DT ==None:
            print("==========generate example========")
            ptK = ptk2 #最前面设置的枚举的反例个数
            ptList = []
            while ptK>0:
                pt = genPtSatFormula(pathFormula,ptList)
                ptList.append(pt)
                ptK = ptK - 1
            print(ptk2," example have generate:",ptList)
            for pt in ptList:
                pts.append(pt)
                ptsOutput.append(genOutput(pt))
            isSAT = False
            print("====================================")
        if isSAT == True:
            print("这条路劲",pathFormula,"找到了可满足决策：")
            print(tree2Act(DT))
            for i in winningStrategyTemp:
               winningStrategy.append(i)
            break
if exitFlag == False:
    Thread2.cancel()
    winningStrategyTime = time.time() - startWinningStrategyTime
    for i in winningStrategy:
        print(i)
    print("winning strategy time:",round(winningStrategyTime,2))

    sheet1.write(row, 3, str(winningStrategy))
    sheet1.write(row, 4, round(winningStrategyTime,2))
    newwb.save(resultFile)

#根据state(满足WF,C) 求出output 两个参数 act[动作序号] parameter[动作参数]
# pts=[]
# ptsOutput=[]


