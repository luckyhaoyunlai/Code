
import threading
import eventlet
from pkg_resources import NullProvider
import xlrd
from subfile.PDDLGrammarLexer import PDDLGrammarLexer
from subfile.PDDLGrammarParser import PDDLGrammarParser
from math import log
from z3 import *
from MyVisitor import MyVisitor
from MyVisitor import game
from opera import *
from antlr4 import *
import time
from xlwt import *
from xlrd import *
from xlutils.copy import copy


X = Int('X')
X1 = Int('X1')
X2 = Int('X2')
Y = Int('Y')
Y1 = Int('Y1')
Y2 = Int("Y2")

k = Int('k')
l = Int('l')
(k1, k2, k3) = Ints('k1 k2 k3')

ptk = 3
"""=================game import========================="""
# pddlFile =sys.argv[1] #由文件main.py输入路径
# resultFile =sys.argv[2]

pddlFile = r"6.29pddl\_Nim\Anther_nim\Two-piled-odd-or-even-nim.pddl"  # 执行单个pddl
resultFile = r"C:\Users\admin\Desktop\result\_625.xls"  # 生成的结果文件

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

print("Var Liat:",varList)

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


"""按大小枚举谓词"""


def enumeratePredicate(MaxSize):
    SigSet = []
    ExpSet = []
    SizeOneExps = []
    Items = []
    ItemsNum = []
    ItemsVar = []

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
    while (li <= MaxSize):
        for i in t_vocabulary:
            if i['Function_name'] == 'Add':
                if li == 2:  # add(var,-)
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

                if li == 2:  # 自己修枝sub 只有li=2时出现
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
        li = li+1

    for i in ExpSet:
        Items.append(i['Expression'])
        if i['Isnum']:
            ItemsNum.append(i['Expression'])
        else:
            ItemsVar.append(i['Expression'])
    print("Items set generate predicate:\n\t", Items)

    # 优化1 如果谓词集合的大小为2^len(pts)则退出 因为已经满足了所有的情况
    # 优化2 如果
    # maxsize=MaxSize+1
    predGoal = []
    for i in p_vocabulary:  # == > >=
        if i['arity'] == 2:
            for choose1 in ItemsVar:
                for choose2 in Items:
                    tempPredicate = FunExg[i['Function_name']](
                        choose1, choose2)
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
                        try:
                            tempPredicate = FunExg[i['Function_name']](
                                choose1, choose2, choose3)
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


"""找到下个term不属于covers的"""


def nextDistinctTerm():
    ptsLength = len(pts)
    if ptsLength == 0:
        cover[0] = []
        return 0
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
                    Goal.append(pt[0])
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
                    Goal.append(pt[1])
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
                                term = FunExg[i['Function_name']](
                                    choose1['Expression'], choose2['Expression'])
                                Goal = []  # 计算goal
                                for k1, h in zip(choose1['outputData'], choose2['outputData']):
                                    Goal.append(
                                        FunExg[i['Function_name']](k1, h))
                                if Goal not in SigSet:  # 更新SigSet ExgSet
                                    SigSet.append(Goal)
                                    i['outputData'] = Goal
                                    ExpSet.append(
                                        {'Expression': term, 'arity': i['arity'], 'outputData': Goal, 'size': MaxSize})
                                    if term not in terms:
                                        # term不在terms才更新cover,且要求最后一个pt必须满足term
                                        for num in range(ptsLength):
                                            if(Goal[num] == ptsGoal[num]):  # 跟新cover[term]
                                                if term not in cover:
                                                    cover[term] = []
                                                if pts[num] not in cover[term]:
                                                    cover[term].append(
                                                        pts[num])
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
    if(Pick_pred == False):  # 谓词不足以去划分
        global DTflag  # 全局变量DTflag来检测是否有树生成
        DTflag = False
        # print('DTflag=', DTflag)
        return None
    root = TreeNode(Pick_pred)
    ptsYes = []
    ptsNo = []
    for pt in pts:
        if ptSatPred(pt, Pick_pred):
            ptsYes.append(pt)
        else:
            ptsNo.append(pt)
    print("Divide two part:\n\t")
    print(ptsYes, ":", ptsNo)
    temp_preds = preds  # 不用深度复制
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
    print("Set of predicates\n\t", preds)
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
        InfoGain = Entropy(pts)-(len(ptsYes)/len(pts)) * \
            Entropy(ptsYes) - (len(ptsNo)/len(pts))*Entropy(ptsNo)
        # print("信息增益",InfoGain)
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
        return "DT为空"
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
    # print("Insert into isLossingstate:")
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
                        print("find example:", v1, v2)
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
        if i>100:
            example_run_out_sign = True
            return 'illegal'
        while True:
            for v1 in range(0, i+1):
                for v2 in range(0, i-v1+1):
                    v3 = i-v1-v2
                    # print("findexample:",v1,v2,v3)
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


def satfindstate(ptk):
    ptK = ptk
    ptList = []
    m = s.model()
    value = []
    for i in Game["varList"]:
        value.append(m[i].as_long())
    if isLossingState(*value) != 'illegal':
        ptK -= 1
        ptList.append(value)
        if(ptK == 0):
            return ptList
    while True:
        pt = FindCountExample(ptList)
        if pt =='illegal':#例子用完了，返回ptList
            return ptList
        if isLossingState(*pt) == 'illegal':
            continue
        else:
            ptK -= 1
            ptList.append(pt)
            if(ptK == 0):
                print("Three example(ptList):\t", ptList)
                return ptList


def unkownfindstate(ptk):
    ptK = ptk
    ptList = []
    while True:
        pt = FindCountExample(ptList)
        if pt =='illegal':#例子用完了，返回ptList
            return ptList
        if isLossingState(*pt) == 'illegal':
            continue
        else:
            ptK -= 1
            ptList.append(pt)
            if(ptK == 0):
                print("Three example(ptList):\t", ptList)
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
    preds = []
    cover[True] = []
    cover[False] = []
    DT = None

    # cover all pt cover={False:[[1],[2]]}
    # print("Example set\t", pts)
    for num in range(len(pts)):
        cover[ptsGoal[num]].append(pts[num])
    print("Cover set:  \t", cover)
    # while(not(isCoverAll())):
    #     terms=terms.append(nextDistinctTerm())
    global DTflag
    DTflag = True
    e = X == X  # 默认表达式
    last_e = e
    DTTime = time.time()
    while(pts != [] and (DT == None or DTflag == False)):
        DTflag = True
        enumPredsTime = time.time()
        enumeratePredicate(Maxsize)
        print("Num of pts:  ", len(pts))
        calculateIGTime = time.time()
        DT = learn_DT(pts, preds)  # lenrnDT中可能会出现 找出不了最好的谓词划分
        # print("Information gain time ：",time.time()-calculateIGTime)
        if(DTflag == False):
            Maxsize += 1
            print('cannot solve,need more predicates,increase Maxsize', Maxsize)
    print("Time of learn DT：", time.time()-DTTime)
    if DT != None:
        e = eval(tree2Expr(DT))
    print("Dicision tree:\n\t", e)
    # if DT != None:
    #     print("Tree transform to normal expression:\n\t",
    #           eval(tree2LossingFormula(DT)))
    # 模拟解--N态
    # e=Not(Or(And(X2==0,X!=X1),And(X2==1,Or(X1-X!=1,X%2==1),Or(X-X1!=1,X1%2==1)),And(X2==2,Or(X-X1!=2,X1%4==2,X1%4==3),Or(X1-X!=2,X%4==2,X%4==3))))

    # e=Not(Or(And(X2==0,X!=X1),And(X2==1,Or(X1-X!=1,X%2==1),Or(X-X1!=1,X1%2==1))))
    # e=And(Or(X2!=0,X==X1),Or(X2!=1,And(X1-X==1,X%2!=1),Or(X-X1==1,X1%2!=1)))
    # e=simplify(e)
    # e=And(Or(X%6==1,X%6==2,X%6==3),Or(X1%6==1,X1%6==2,X1%6==3),Or(X2%6==1,X2%6==2,X2%6==3))#2.6
    e1 = eval(str(e).replace("X1", "Y1").replace("X2", "Y2").replace("X", "Y"))
    print("Add expression to verity:\n", e)
    if str(e) != str(last_e):
        if Game["type"] == "normal" :
            con1 = And(Game["Terminal_Condition"], Not(e))
            con2 = And(Game["Constraint"], Not(e), ForAll(
                [Y, Y1, Y2], Or(Not(global_transition_formula), Not(e1))))
            con3 = And(Game["Constraint"], e, Exists(
                [Y, Y1, Y2], And(global_transition_formula, e1)))
        else:
            con1 = And(Game["Terminal_Condition"], e)
            con2 = And(Game["Constraint"], Not(e), Not(Game["Terminal_Condition"]), ForAll(
                [Y, Y1, Y2], Or(Not(global_transition_formula), Not(e1))))
            con3 = And(Game["Constraint"], e, Exists(
                [Y, Y1, Y2], And(global_transition_formula, e1)))
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
                    lossing_formula = eval(tree2LossingFormula(DT))
                    print("Loosing formula：", lossing_formula)
                    losing_formula_Y = e1
                    winning_formula = simplify(Not(lossing_formula))
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
                    newwb.save(resultFile)

                    # fp = open(resultFile, 'a')
                    # fp.write(pddlFile.split('\\')[-1]+"\t")
                    # fp.write(str(simplify(Not(lossing_formula))) +
                    #          "\t"+winning_formula_time+"\n")
                    Thread1.cancel()  # 取消计时线程
                    break
    else:
        print("repeat expression")
        examples = unkownfindstate(ptk)
    print("one time generate examples:", examples)
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

    #     if(s.check()==unsat):
    #         print("unsat SMT判断所用时间：",time.time()-smttime)
    #         # losing_formula = e
    #         # print("树的表达式：",tree2LossingFormula(DT))
    #         lossing_formula=eval(tree2LossingFormula(DT))
    #         print("必败公式是：",lossing_formula)
    #         losing_formula_Y = e1
    #         print("-----------------------------")
    #         winning_formula_time = time.time()-start_winning_formula_time
    #         print("必胜公式是：",simplify(Not(lossing_formula)))
    #         print("花费的时间是：",winning_formula_time)
    #         break
    #     elif(s.check()==unknown):
    #         print("unkown SMT判断所用时间：",time.time()-smttime)
    #         if (Game["var_num"] == 1):
    #             num4 = FindCountExample(e)
    #         if (Game["var_num"] == 2):
    #             num4, num5 = FindCountExample(e)
    #     else: #优化 可以把sat给计算出来

    #         m=s.model()
    #         if (Game["var_num"] == 1):
    #             num4 = m[X].as_long()
    #             if isLossingState(num4) == 'illegal':
    #                 num4 = FindCountExample(e)
    #         if (Game["var_num"] == 2):
    #             num4 = m[X].as_long()
    #             num5 = m[X1].as_long()
    #             #1如果解违法 找新的 2如果解重复，找新的
    #             if isLossingState(num4,num5) == 'illegal':
    #                 num4, num5 = FindCountExample(e)
    #             else:
    #                 flags=False
    #                 for pt in pts:
    #                     if(pt[c]==num4 and pt[d]==num5):
    #                         flags=True
    #                         break
    #                 if flags==True:
    #                     num4,num5=FindCountExample(e)
    # else:#SMT解决不了这个问题 导致解还是和之前的一样
    #     if (Game["var_num"] == 1):
    #         num4 = FindCountExample(e)
    #     if (Game["var_num"] == 2):
    #         num4, num5 = FindCountExample(e)
    # if (Game["var_num"] == 1):
    #     print("反例点",num4)
    # if(Game["var_num"]==2):
    #     print("反例点",num4,num5)
    # if (Game["var_num"] == 1):
    #     if {c: num4} not in pts:
    #         pts.append({c: num4})
    #         ptsGoal.append(isLossingState(num4))
    # if (Game["var_num"] == 2):
    #     if {c: num4, d: num5} not in pts:
    #         pts.append({c: num4, d: num5})
    #         ptsGoal.append(isLossingState(num4,num5))

# print("开始测试")
# e=(X1-X)%3==1
# e1=eval(str(e).replace("X1","Y1").replace("X","Y"))
# s=Solver()
# s.add(Or(And(Game["Terminal_Condition"], Not(e)),  # normal
#          And(Game["Constraint"],Not(e),ForAll([Y,Y1],Or(Not(global_transition_formula),Not(e1)))),
#          And(Game["Constraint"],e,Exists([Y,Y1],And(global_transition_formula,e1)))))
# s.add(Or(And(Game["Terminal_Condition"], e),  # misere
#          And(Game["Constraint"],Not(e),Not(Game["Terminal_Condition"]),ForAll([Y,Y1],Or(Not(global_transition_formula),Not(e1)))),
#          And(Game["Constraint"],e,Exists([Y,Y1],And(global_transition_formula,e1)))))
# print(s.check())
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
#         specificationTemp=eval(str(specificationTemp).replace(str(k), '('+str(e)+')'))  # 枚举的结果代替要求的未知数

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
