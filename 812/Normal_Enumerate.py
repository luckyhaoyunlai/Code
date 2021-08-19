import sys
from antlr4 import *
from pkg_resources import SOURCE_DIST
from subfile.PDDLGrammarLexer import PDDLGrammarLexer
from subfile.PDDLGrammarParser import PDDLGrammarParser
from z3 import *
from MyVisitor import MyVisitor
from MyVisitor import game
from z3 import *
from opera import *
import copy
import time
import eventlet#导入eventlet这个模块


start_total = time.time()

# 变量，要用在z3检验过程中的
X = Int('X')
Y = Int('Y')
X1 = Int('X1')
Y1 = Int('Y1')
k = Int('k')
l=Int('l')

c = Int('c')
d = Int('d')



# pddlFile =sys.argv[1]
pddlFile="pddl1\Subtraction_game\Take-away\Take-away-2.pddl"
resultFile="result.txt"
fp=open(resultFile,'a')
fp.write(pddlFile.split('\\')[-1]+"\t")

input_stream = FileStream(pddlFile) 
lexer = PDDLGrammarLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = PDDLGrammarParser(token_stream)
tree = parser.domain()
s = Solver()  
visitor = MyVisitor()
visitor.visit(tree) 

Terminal_Condition=eval(str(game.tercondition).replace('v1','X').replace('v2','X1'))
Constarint=eval(str(game.constraint).replace('v1','X').replace('v2','X1'))
varList = []
for i in game.var_list:
    i=str(i).replace('v1','X').replace('v2','X1')
    varList.append(eval(i))
actions=[]

for i in game.action_list:
    one={"action_name":i[0],
         "precondition":eval(str(i[2]).replace('v1','X').replace('v2','X1')),
         "transition_formula":eval(str(i[3]).replace('v1\'','Y').replace('v2\'','Y1').replace('v1','X').replace('v2','X1')) }
    actions.append(one)
Game = {"Terminal_Condition":Terminal_Condition,
        "varList":varList,
        "actions": actions,
        "Constraint":Constarint,
        "var_num":game.objectsCount,
        "type":"misere",           
        "appeal_constants": game.constantList}  
# -----------------------------------------------------------------

vocabulary = [{'Input': ['Int', 'Int'], 'Output':'Int', 'Function_name':'Add', 'arity':2},
              {'Input': ['Int', 'Int'], 'Output': 'Int','Function_name': 'Sub', 'arity':2},
              {'Input': ['Int'], 'Output': 'Int','Function_name': 'Inc', 'arity':1},
              {'Input': ['Int'], 'Output': 'Int', 'Function_name': 'Dec', 'arity':1},
              {'Input': ['Int', 'Int'], 'Output': 'Bool','Function_name': 'Equal', 'arity': 2},
              {'Input': ['Int', 'Int'], 'Output': 'Bool','Function_name': 'Unequal', 'arity': 2},
              {'Input': ['Int', 'Int'], 'Output': 'Bool','Function_name': 'Ge', 'arity':2},
              {'Input': ['Int', 'Int'], 'Output': 'Bool', 'Function_name': 'Gt', 'arity':2},
              {'Input': ['Bool', 'Bool'], 'Output': 'Bool','Function_name': 'OR', 'arity': 2},
              {'Input': ['Bool', 'Bool'], 'Output': 'Bool','Function_name': 'AND', 'arity': 2},
              {'Input': [], 'Output': 'Int', 'Function_name': 'number0', 'arity': 0},
              {'Input': [], 'Output': 'Int', 'Function_name': 'number1', 'arity': 0},
              {'Input': ['Int', 'Int', 'Int'], 'Output':'Bool', 'Function_name':'ModTest', 'arity':3}]

# 想加入基本的常数，就添加的字典中，根据游戏的特性决定
# for i in Game["appeal_constants"]:
#     eval('def Number'+i+'():return '+i+';')
#     numFunc[i]='Number'+str(i)
#     vocabulary.append({'Input': [], 'Output': 'Int','Function_name':'Number'+str(i), 'arity': 0})
for i in Game["appeal_constants"]:
    vocabulary.append({'Input': [], 'Output': 'Int',
                       'Function_name': 'number'+i, 'arity': 0})

# The goal that the enumerate algorithm generated
goal = {'value': [], 'type': ''}
# 函数名称字典，调用是加个（）即可表示具体的函数
FunExg = {'Add': Add, 'Sub': Sub, 'Inc': Inc, 'Dec': Dec, 'Ge': Ge,
          'Gt': Gt, 'OR': OR, 'AND': AND, 'NOT': NOT, 'Equal': Equal, 'Mod': Mod,
          'Unequal': Unequal, 'X': X, 'Y': Y, 'number0': number0, 'number1': number1, 'ModTest': ModTest}
# 存在两个变量就添加到funexg中，之后好调用
if(Game["var_num"] == 2):
    FunExg['X1'] = X1
    FunExg['Y1'] = Y1
# eval字符串方式输入表达式给z3solver
Z3FunExg = {'Add': Add, 'Sub': Sub, 'Inc': Inc, 'Dec': Dec, 'Ge': Ge,
            'Gt': Gt, 'OR': z3OR, 'AND': z3AND, 'NOT': z3NOT, 'Equal': Equal, 'Mod': Mod,
            'Unequal': Unequal, 'X': X, 'Y': Y, 'number0': number0, 'number1': number1, 'ModTest': ModTest}
if(Game["var_num"] == 2):
    Z3FunExg['X1'] = X1
    Z3FunExg['Y1'] = Y1
for i in Game["appeal_constants"]:
    FunExg['number'+i] = eval('number'+i)

ConcreteExs = []  # 反例集合

start_winning_formula_time = time.time()

# The enumerative algorithm for multiple objects
# [X==X,Y==Y]
# 枚举算法 输入vocabulation,concreteExs,sizeoneEXps,
# 输出e满足反例集合 z3表达式

# E_A(num,'Bool')  Enumerate_algorithm(it_mum,'Int')
def Enumerate_algorithm(count, Goal_type):
    goal['type'] = Goal_type
    SigSet = []   # signatures 记录是否枚举过了 (e,concreteEXp)  [2,2,2,2]反例集合几个数就大小多少
    ExpSet = []  # set of expression（type t size i）
    SizeOneExps = []
    # 初始化大小为1的表达式  arity变量数目 size输出的大小
    SizeOneExps.append({'Input': ['Int'], 'Output': 'Int', 'Expression': 'X', 'z3Expression': [
                       X, Y], 'arity': 1, 'size': 1})
    if(Game["var_num"] == 2):
        SizeOneExps.append({'Input': ['Int'], 'Output': 'Int', 'Expression': 'X1', 'z3Expression': [
                           X1, Y1], 'arity': 1, 'size': 1})
    SizeOneExps.append({'Input': [], 'Output': 'Int', 'Expression': 'number0',
                        'z3Expression': [number0(), number0()], 'arity': 0, 'size': 1})
    SizeOneExps.append({'Input': [], 'Output': 'Int', 'Expression': 'number1',
                        'z3Expression': [number1(), number1()], 'arity': 0, 'size': 1})
    for i in Game["appeal_constants"]:
        SizeOneExps.append({'Input': [], 'Output': 'Int', 'Expression': 'number'+i, 'z3Expression': [
                           eval('number'+i)(), eval('number'+i)()], 'arity': 0, 'size': 1})
    # 先枚举大小1的表达式（常数，单个变量），看是否满足goal
    for i in SizeOneExps:
        Goal1 = []
        if (i['arity'] == 0):  # 数字
            for num in range(count):  # count反例数
                Goal1.append(FunExg[i['Expression']]())
            if Goal1 not in SigSet:  # Sigset标记
                SigSet.append(Goal1)
                i['Output_data'] = Goal1
                ExpSet.append(i)  # 表达式添加一个输出项，将表达式加到表达式集合中
                if Goal1 == goal['value'] and i['Output'] == goal['type']:
                    return i['z3Expression']   # z3 [0,0] [1,1]
        else:
            if i['Expression'] == 'X':  # 开始时反例集合为空
                # 反例[{"Input":{c:2,d:2}, "Output":Bool}...]致胜公式
                for j in ConcreteExs:
                   # 反例[{'Input': {c: 3, d: 0}, 'Output': 2}] 致胜策略
                   # X<-c   x1<-d
                    # print(ConcreteExs)
                    O = j['Input'][c]  # sizeone只有c没有d
                    Goal1.append(O)
                if Goal1 not in SigSet:
                    SigSet.append(Goal1)  # SigSet 保留不同的Goal1
                    i['Output_data'] = Goal1
                    ExpSet.append(i)  # size_one_表达式 添加到 EXPset
                    if Goal1 == goal['value'] and i['Output'] == goal['type']:  # 检验是否和goal相等
                        return i['z3Expression']  # [X,Y]
            if i['Expression'] == 'X1':
                for j in ConcreteExs:
                    O = j['Input'][d]  # d
                    Goal1.append(O)
                if Goal1 not in SigSet:
                    SigSet.append(Goal1)
                    i['Output_data'] = Goal1
                    ExpSet.append(i)
                    if Goal1 == goal['value'] and i['Output'] == goal['type']:
                        #print(i['z3Expression']) [X1,Y1]
                        return i['z3Expression']

    for i in vocabulary:
        if (i['arity'] == 1):  # Inc Dec
            # print('199',ExpSet)
            for j in ExpSet:
                if j['size'] == 1:  # 只能取1的表达式来进行+1-1
                    Goal1 = []    #
                    if (i['Input'][0] == j['Output']):  # 要求他们的类型相同
                        TempExp = i['Function_name'] + \
                            '(' + j['Expression'] + ')'  # Inc(x) 是个字符串
                        z3TempExp1 = Z3FunExg[i['Function_name']](
                            j['z3Expression'][0])  # x+1  X是Int('x')
                        z3TempExp2 = Z3FunExg[i['Function_name']](
                            j['z3Expression'][1])  # x+1
                        for ki in j['Output_data']:  # [] [2] [2 2] [2 2 1] [2, 2, 1, 2]
                            O = FunExg[i['Function_name']](ki)
                            Goal1.append(O)
                        if Goal1 not in SigSet:  # 更新sigset
                            SigSet.append(Goal1)  # 存储枚举的结果的挂号
                            ExpSet.append(
                                {'Input': i['Input'], 'Output': i['Output'], 'Expression': TempExp,
                                 'z3Expression': [z3TempExp1, z3TempExp2], 'arity': i['arity'],
                                 'size': 2, 'Output_data': Goal1})
                            # print("215 expset:",ExpSet)
                        if Goal1 == goal['value'] and i['Output'] == goal['type']:
                            return [z3TempExp1, z3TempExp2]
    li = 3  # 表达式的大小
    while (True):  # 从3开始，找不到一直循环，i+=1
        for i in vocabulary:
            m = i['arity']
            if (m == 1):  # Inc Dec
                for j in ExpSet:
                    try:
                        Goal1 = []
                        if ((j['size'] == li - 1) and (i['Input'] == j['Output'])):
                            TempExp = i['Function_name'] + \
                                '(' + j['Expression'] + ')'  # Inc(x)
                            z3TempExp1 = Z3FunExg[i['Function_name']](
                                j['z3Expression'][0])
                            z3TempExp2 = Z3FunExg[i['Function_name']](
                                j['z3Expression'][1])  # [x+1,x+1]
                            for ki in j['Output_data']:
                                O = FunExg[i['Function_name']](ki)
                                Goal1.append(O)
                            if Goal1 not in SigSet:  # 跟新Sigset才更型ExpSet
                                SigSet.append(Goal1)
                                ExpSet.append({'Input': i['Input'], 'Output': i['Output'],
                                               'Expression': TempExp, 'z3Expression': [z3TempExp1, z3TempExp2],
                                               'arity': i['arity'], 'size': li, 'Output_data': Goal1})
                            # 检验是否满足反例集合
                            if Goal1 == goal['value'] and i['Output'] == goal['type']:
                                return [z3TempExp1, z3TempExp2]
                    except ZeroDivisionError:
                        pass
                    continue
            elif (m == 2):
                for num1 in range(1, li - 1):  # 遍历num1+num2=li-1的值
                    for num2 in range(1, li - 1):
                        if (num1 + num2 == li - 1):
                            for choose1 in ExpSet:  # 遍历ExpSet要求size1=num1 size2=num2
                                if (choose1['size'] == num1):
                                    for choose2 in ExpSet:
                                        if (choose2['size'] == num2):
                                            if ((i['Input'][0] == choose1['Output']) and (  # 条件是两输入的类型必须满足输出的
                                                    i['Input'][1] == choose2['Output'])):
                                                try:
                                                    Goal1 = []
                                                    TempExp = ''
                                                    # add(x,y)
                                                    TempExp = i['Function_name'] + \
                                                        '(' + choose1['Expression'] + \
                                                        ',' + \
                                                        choose2['Expression'] + ')'
                                                    z3TempExp1 = Z3FunExg[i['Function_name']](
                                                        choose1['z3Expression'][0], choose2['z3Expression'][0])
                                                    z3TempExp2 = Z3FunExg[i['Function_name']](
                                                        choose1['z3Expression'][1], choose2['z3Expression'][1])
                                                    # 更型Goal1 zip成（a，b）
                                                    for ki, h in zip(choose1['Output_data'], choose2['Output_data']):
                                                        O = FunExg[i['Function_name']](ki, h)
                                                        # print('258',i['Function_name'],choose1['Expression'],choose1['Output_data'],choose2['Expression'],choose2['Output_data'],O)
                                                        # goal={e,concertExs}  [True, True, True]
                                                        Goal1.append(O)
                                                    # print('260',Goal1)
                                                    if Goal1 not in SigSet:
                                                        SigSet.append(Goal1)
                                                        ExpSet.append(
                                                            {'Input': i['Input'], 'Output': i['Output'],
                                                             'Expression': TempExp, 'z3Expression': [z3TempExp1, z3TempExp2],
                                                             'arity': i['arity'], 'size': li, 'Output_data': Goal1})
                                                    # print(SigSet)
                                                    if Goal1 == goal['value'] and i['Output'] == goal['type']:
                                                        # print(ExpSet)
                                                        return [z3TempExp1, z3TempExp2]
                                                except ZeroDivisionError:
                                                    pass
                                                continue
            elif (m == 3):  # 只有ModTest操作
                if (i['Function_name'] == 'ModTest'):
                    for num1 in range(1, li - 1):
                        for num2 in range(1, li - 1):
                            for num3 in range(1, li - 1):
                                if (num1 + num2 + num3 == li - 1):  # 遍历出合适的num1,num2,num3
                                    for choose1 in ExpSet:
                                        if (choose1['size'] == num1):
                                            for choose2 in ExpSet:
                                                if (choose2['size'] == num2):
                                                    for choose3 in ExpSet:
                                                        # 遍历出三个大小合适的表达式
                                                        if (choose3['size'] == num3 and choose3['arity'] == 0):
                                                            if ((i['Input'][0] == choose1['Output']) and (i['Input'][1] == choose2['Output']) and (i['Input'][2] == choose3['Output'])):
                                                                try:
                                                                    Goal1 = []
                                                                    TempExp = ''
                                                                    TempExp = i['Function_name'] + '(' + choose1['Expression'] + \
                                                                        ',' + \
                                                                        choose2['Expression'] + ',' + \
                                                                        choose3['Expression'] + ')'
                                                                    z3TempExp1 = Z3FunExg[i['Function_name']](
                                                                        choose1['z3Expression'][0], choose2['z3Expression'][0], choose3['z3Expression'][0])
                                                                    z3TempExp2 = Z3FunExg[i['Function_name']](
                                                                        choose1['z3Expression'][1], choose2['z3Expression'][1], choose3['z3Expression'][1])
                                                                    for ki, h, g in zip(choose1['Output_data'], choose2['Output_data'], choose3['Output_data']):
                                                                        O = FunExg[i['Function_name']](
                                                                            ki, h, g)
                                                                        Goal1.append(
                                                                            O)
                                                                    if Goal1 not in SigSet:
                                                                        SigSet.append(
                                                                            Goal1)
                                                                        ExpSet.append({'Input': i['Input'], 'Output': i['Output'],
                                                                                       'Expression': TempExp, 'z3Expression': [z3TempExp1, z3TempExp2],
                                                                                       'arity': i['arity'], 'size': li, 'Output_data': Goal1})
                                                                    if Goal1 == goal['value'] and i['Output'] == goal['type']:
                                                                        return [z3TempExp1, z3TempExp2]
                                                                except ZeroDivisionError:
                                                                    pass
                                                                continue
                else:
                    for num1 in range(1, li - 1):
                        for num2 in range(1, li - 1):
                            for num3 in range(1, li - 1):
                                if (num1 + num2 + num3 == li - 1):
                                    for choose1 in ExpSet:
                                        if (choose1['size'] == num1):
                                            for choose2 in ExpSet:
                                                if (choose2['size'] == num2):
                                                    for choose3 in ExpSet:
                                                        if (choose3['size'] == num3):
                                                            if ((i['Input'][0] == choose1['Output']) and (i['Input'][1] == choose2['Output']) and (i['Input'][2] == choose3['Output'])):
                                                                try:
                                                                    Goal1 = []
                                                                    TempExp = ''
                                                                    TempExp = i['Function_name'] + '(' + choose1['Expression'] + \
                                                                        ',' + \
                                                                        choose2['Expression'] + ',' + \
                                                                        choose3['Expression'] + ')'
                                                                    z3TempExp1 = Z3FunExg[i['Function_name']](
                                                                        choose1['z3Expression'][0], choose2['z3Expression'][0], choose3['z3Expression'][0])
                                                                    z3TempExp2 = Z3FunExg[i['Function_name']](
                                                                        choose1['z3Expression'][1], choose2['z3Expression'][1], choose3['z3Expression'][1])
                                                                    for ki, h, g in zip(choose1['Output_data'], choose2['Output_data'], choose3['Output_data']):
                                                                        O = FunExg[i['Function_name']](
                                                                            ki, h, g)
                                                                        # print('327',O)
                                                                        Goal1.append(
                                                                            O)
                                                                    if Goal1 not in SigSet:
                                                                        SigSet.append(
                                                                            Goal1)
                                                                        ExpSet.append({'Input': i['Input'], 'Output': i['Output'],
                                                                                       'Expression': TempExp, 'z3Expression': [z3TempExp1, z3TempExp2],
                                                                                       'arity': i['arity'], 'size': li, 'Output_data': Goal1})
                                                                    if Goal1 == goal['value'] and i['Output'] == goal['type']:
                                                                        return [z3TempExp1, z3TempExp2]
                                                                except ZeroDivisionError:
                                                                    pass
                                                                continue
        li = li+1
        # if(li > 8):
        #     print("此时枚举得size超过了我设置得最大size8,停止枚举，返回False:")
        #     return False
# 全局转换公式
global_transition_formula = "Or("
for i in Game["actions"]:
    if "k" in str(i["transition_formula"]) :
        global_transition_formula = global_transition_formula + "Exists(k,"+str(i["transition_formula"])+"),"
    else:
        global_transition_formula = global_transition_formula + str(i["transition_formula"])+","

global_transition_formula = global_transition_formula[:-1]
global_transition_formula = global_transition_formula+")"

print("Global transfer formula：",global_transition_formula)
global_transition_formula = simplify(eval(global_transition_formula))

position_1 = []
for i in range(0, 100):
    position_1.append('illegal')

position_2 = []
for i in range(0, 100):
    position_2.append([])
    for j in range(0, 100):
        position_2[i].append('illegal')

s = Solver()
s.add(Game["Terminal_Condition"])
s.check()
m = s.model()
if(Game["var_num"] == 1):
    if(Game["type"]=="normal"):
        position_1[m[X].as_long()] = True  #普通版本终态时必败态为True
    else:
        position_1[m[X].as_long()] = False #misere版本
if(Game["var_num"] == 2):
    if(Game["type"]=="normal"):
        position_2[m[X].as_long()][m[X1].as_long()] = True
    else:
        position_2[m[X].as_long()][m[X1].as_long()] = False


def isLossingState(*v):  # 接受1或者2个参数的元组 根据终结条件去判断是否是lossing_state 其他更多参数的游戏再修改
    for i in v:
        if i>=100:
            return 'illegal'
    if (len(v) == 1):
        if (position_1[v[0]] != 'illegal'):
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
        return position_1[v[0]]
    if(len(v) == 2):
        if(position_2[v[0]][v[1]] != 'illegal'):
            return position_2[v[0]][v[1]]
        for x in range(0, v[0]+1):  # 遍历所有的点（x，y）去查看状态
            for y in range(0, v[1]+1):
                if(position_2[x][y] != 'illegal'):
                    continue
                temp = []  # 存放转移后的解
                while (True):
                    s = Solver()
                    s.add(global_transition_formula)
                    s.add(Game["Constraint"])
                    s.add(X == x, X1 == y)  # 满足就是说

                    for i in temp:
                        s.add(Or(Y != i[0], Y1 != i[1]))

                    if (s.check() == sat):  # p态
                        m = s.model()
                        temp.append([m[Y].as_long(), m[Y1].as_long()])
                    else:
                        break
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
        return position_2[v[0]][v[1]]

# This function aims to enumerate states in an increasing order of the sum of values
#  of all state variables until find a suitable state
# 此函数旨在按值和的递增顺序枚举状态
# 直到找到合适的状态


def FindCountExample(ptList):
    if (Game["var_num"] == 1):
        i = 2
        while(True):
            for v1 in range(0, i):
                if [v1] not in ptList:
                    flag12 = False
                    for pt in ConcreteExs:
                        if (v1 == pt["Input"][c]):
                            flag12 = True
                    if flag12 == False:
                        s = Solver()
                        s.add(Game["Constraint"])
                        s.add(X == v1)
                        if (s.check() == sat):
                            return [v1]
                        else:
                            continue
            i = i + 1
    if(Game["var_num"] == 2):
        i = 2
        while(True):
            for v1 in range(0, i):
                for v2 in range(0, i):
                    if [v1,v2] not in ptList:
                        if v1+v2 == i:  # 遍历所有的v1v2=i的组合 按照size遍历
                            flag12 = False
                            # 改成 pt={c:v1,d:v2} if pt not in ConcreteExs:
                            for pt in ConcreteExs:
                                if (v1 == pt["Input"][c] and v2 == pt["Input"][d]):
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
                                    # boolTemp = isLossingState(v1, v2)
                                    # boolTemp2 = eval(str(expr).replace(str(X1), str(v2)).replace(str(X), str(v1)))
                                    # s = Solver()
                                    # if boolTemp == False:
                                    #     s.add(True, boolTemp2)
                                    #     if(s.check() == sat):
                                    #         return v1, v2
                                    # elif boolTemp == True:
                                    #     s.add(True, boolTemp2)
                                    #     if(s.check() == unsat):
                                        return [v1,v2]
                                else:
                                    continue
            i = i+1


e = 1
num = 1
num1 = 0
flag = 1
O = Bool('O')


def satfindstate():
    ptK = 3 #每轮生成的反例个数
    ptList = []
    m=s.model()
    value=[] #一个pt
    for i in Game["varList"]: #求所有变量的解
        value.append(m[i].as_long())
    print("求得的解：",value)
    if isLossingState(*value)!='illegal':
        ptK-=1
        ptList.append(value)
        if(ptK==0):return ptList
    while True:
        pt=FindCountExample(ptList)
        print("pt",pt)
        if isLossingState(*pt)=='illegal':
            continue
        else:
            ptK-=1
            ptList.append(pt)       #[(1,2),(2,3)...]
            if(ptK==0):
                print("ptList",ptList)
                return ptList
def unkownfindstate():
    ptK = 3 #每轮生成的反例个数
    ptList = []
    while True:
        pt=FindCountExample(ptList)
        if isLossingState(*pt)=='illegal':
            continue
        else:
            ptK-=1
            ptList.append(pt)
            if(ptK==0):
                return ptList


while(True):  # 合成制胜公式
    last_e = e
    # 枚举的是必败条件的表达式[X == X, Y == Y] [X != X1, Y != Y1] [X == X1 + 1, Y == Y1 + 1]....
    e = Enumerate_algorithm(num, 'Bool')
    # e=[(X + X1)%3 == 0, (Y + Y1)%3 == 0]
    print("expression of enumerate result：", e)
    print("Counter example set:",end=' ')
    for i in ConcreteExs:
        print(i['Input'],i['Output'],end=' ')
    print("len of pts ",len(ConcreteExs))

    if(e != last_e):
        if(Game["type"]=="normal"):
            con1=And(Game["Terminal_Condition"], Not(e[0]))
            con2=And(Game["Constraint"],Not(e[0]),ForAll([Y,Y1],Or(Not(global_transition_formula),Not(e[1]))))
            con3=And(Game["Constraint"],e[0],Exists([Y,Y1],And(global_transition_formula,e[1])))
        elif(Game["type"]=="misere"):
            con1=And(Game["Terminal_Condition"], e[0])
            con2=And(Game["Constraint"],Not(e[0]),Not(Game["Terminal_Condition"]),ForAll([Y,Y1],Or(Not(global_transition_formula),Not(e[1]))))
            con3=And(Game["Constraint"],e[0],Exists([Y,Y1],And(global_transition_formula,e[1])))    
        s = Solver()
        s.add(con1)
        s.set('timeout', 60000)
        if(s.check() == sat):  
            examples=satfindstate()
        # elif(s.check() == unknown): 
        #     examples=unkownfindstate()
        else:                          
            print("condition1 sat")
            s = Solver()
            s.add(con2)
            s.set('timeout', 60000)

            if(s.check() == sat): 
                examples=satfindstate()
            # elif(s.check() == unknown):
            #     examples=unkownfindstate()
            else:                      
                print("condition2 sat")
                s = Solver()
                s.add(con3)
                s.set('timeout', 60000)
                if(s.check() == sat): 
                    examples=satfindstate()
                # elif(s.check() == unknown):
                #     examples=unkownfindstate()
                else:                
                    print("condition3 sat")
                    losing_formula = e[0]
                    losing_formula_Y = e[1]
                    print( '-----------------------------------------------------------------------------')
                    print("The Winning formula of this game is:", Not(losing_formula))
                    generate_winning_formula_time = (time.time() - start_winning_formula_time)
                    print("Time to generate the winning formula:",generate_winning_formula_time)
                    generate_winning_formula_time=str(round(generate_winning_formula_time,2))
                    fp=open(resultFile,'a')
                    fp.write(str(simplify(Not(losing_formula)))+"\t"+generate_winning_formula_time+"\n")
                    break
    else:  
        examples=unkownfindstate()
        print("formula repeat")
    if (Game["var_num"] == 1):
        for i in examples:
            if {'Input': {c: i[0]}, 'Output': isLossingState(i[0])} not in ConcreteExs:
                ConcreteExs.append(
                    {'Input': {c: i[0]}, 'Output': isLossingState(i[0])})
                goal['value'].append(isLossingState(i[0]))
                num = num + 1
    if (Game["var_num"] == 2):
        for i in examples:
            if ({'Input': {c: i[0], d: i[1]}, 'Output': isLossingState(i[0], i[1])}) not in ConcreteExs:
                ConcreteExs.append({'Input': {c: i[0], d: i[1]}, 'Output': isLossingState(i[0], i[1])})
                goal['value'].append(isLossingState(i[0], i[1]))
                num = num + 1
                print('617:',goal)

# ------------------------------------------------------------------


def Losing_formula():
    # return (X + X1) % 3 == 0 #直接输入结果快速测试分块
    return losing_formula


def Winning_formula():
    return Not(losing_formula)
    # return Not((X + X1) % 3 == 0)#直接输入结果快速测试分块


def Losing_formula_Y():
    # return (Y + Y1) % 3 == 0#直接输入结果快速测试分块
    return losing_formula_Y


def Winning_formula_Y():
    # return Not((Y + Y1) % 3 == 0)#直接输入结果快速测试分块
    return Not(losing_formula_Y)


start_refine = time.time()

# The following function aim to refine the winning formula, it will return the covers of winning formula
# 以下函数的目的是细化优胜公式，返回致胜公式的覆盖


def refine_the_winning_formula(Losing_formula):
    C = str(Losing_formula)
    # print('612',C)    X == X1 + 1
    C = C.replace(' ', '')  # X==X1+1
    Ct = []
    # gou'zhao
    if (C.find('And') == -1 and C.find('Or') == -1):  # 表达式没有and or
        if (C.find('==') != -1 and (type(eval(C[(C.find('==') + 2):])) == type(1)) and C.find('%') == -1):
            Ct = []
            Ct.append(C.replace('==', '<'))
            Ct.append(C.replace('==', '>'))
        elif (C.find('==') != -1 and (type(eval(C[(C.find('==') + 2):])) == type(X)) and C.find('%') == -1):
            Ct = []
            Ct.append(C.replace('==', '<'))
            Ct.append(C.replace('==', '>'))
        # a%b==c
        elif (C.find('%') != -1 and (type(eval(C[(C.find('==') + 2):])) == type(1))):
            Ct = []
            num = eval(C[(C.find('%') + 1):C.find('==')]) - 1  # b
            num_original = eval(C[(C.find('==') + 2):])  # c
            while (num >= 0):
                if (num != num_original):  # b!=c and b>=0
                    C = C[:C.find('==') + 2]
                    C = C + str(num)     # a+b
                    Ct.append(C)
                    # Ct.append(C.replace(C[(C.find('==') + 2):], str(num)))
                num = num - 1
    else:
        if ((C.find('X') != -1 and C.find('X1') == -1) or (C.find('X') == -1 and C.find('X1') != -1)):
            if (C.find('%') != -1 and (type(eval(C[(C.find('==') + 2):C.find(',')])) == type(1)) and C.find(
                    'Or') != -1):
                Ct = []
                num = eval(C[(C.find('%') + 1):C.find('==')]) - 1
                prnum = []
                pre = C.find('==')
                while (pre != -1):
                    prnum.append(eval(C[pre + 2]))
                    pre = C.find('==', pre + 1)
                # print(prnum)
                while (num >= 0):
                    if (num not in prnum):
                        Ct.append(C[C.find('X'):C.find(',')].replace(
                            C[C.find('==') + 2], str(num)))
                    num = num - 1
        else:
            if (C.find('And') != -1):
                C1 = C
                C1 = C1.replace('And', 'Or')
                C1 = C1.replace('==', '!=')
                C1 = C1.replace('Or(', '')
                C1 = C1.replace(')', '')
                Ct = C1.split(',')
    refine_time_used = (time.time() - start_refine)
    print("Refine Time used:", refine_time_used)
    print("Covers of this game:", Ct)
    refinement = []
    for i in Ct:
        i = eval(i)
        refinement.append(i)
    return refinement, refine_time_used

# This function is an recursive algorithm that to find the corresponding action parameter of a state
# 此函数是一种递归算法，用于查找状态的相应动作的K值,找不到返回“no suitable k_num”


def f_strategy(action_precondition, action_transition_formula, action_constraint, *v):  # 相当于代入SMT中
    s = Solver()
    s.add(Not(Winning_formula_Y()))
    s.add(action_precondition)
    s.add(action_transition_formula)
    s.add(action_constraint)
    s.add(X == v[0])
    if(Game["var_num"] == 2):
        s.add(X1 == v[1])
    #     print("700",v[0],v[1])
    # print(s.check());
    if(s.check() == sat):  # 添加所有的条件判断是解是否合理
        m = s.model()
        return m[k].as_long()  # 求解出k值
    else:
        return "no suitable k"

# This function aims to enumerate states in an increasing order of the sum of values
#  of all state variables until find a suitable state
# 此函数旨在按值和的递增顺序枚举状态
# 直到找到合适的状态


def findnum_strategy(cover, ConcreteExs, action_constraint):
    s = Solver()
    s.add(cover)
    s.add(action_constraint)
    if(Game["var_num"] == 1):
        for i in ConcreteExs:
            s.add(Or(X != i['Input'][c]))
    if(Game["var_num"] == 2):
        for i in ConcreteExs:
            s.add(Or(X != i['Input'][c], X1 != i['Input'][d]))
    s.check()
    m = s.model()
    if(Game["var_num"] == 1):
        return m[X].as_long()
    if (Game["var_num"] == 2):
        return m[X].as_long(), m[X1].as_long()


Winning_strategy = []
refinement, refine_time_used = refine_the_winning_formula(Losing_formula())

# refinement, refine_time_used = refine_the_winning_formula("(X + X1)%3 == 0")测试用例

# The following is the process of generating the winning strategy for every covers of winning formula
# This process will choose the corresponding action and action parameter of every cover
# 下面是为每个获胜公式的块生成制胜策略的过程
# 此过程将选择每个块对应的动作和动作参数

for cover in refinement:
    print("725cover*******************************************************************************************:", cover)
    s = Solver()
    if(type(cover) == type("")):
        cover = eval(cover)
    # print(cover, type(cover))
    s.add(cover)
    s.add(Game["Constraint"])
    # 判断是否cover能够满足动作的前提
    if(s.check() == unsat):
        continue
    # The type of the initial search target is int
    # 初始搜索的目标是int
    ConcreteExs.clear()
    goal = {'value': [], 'type': ''}
    goal['type'] = 'Int'  # 去枚举int型的表达式 如eat(X) eat(1)
    flag_strategy = False  # 判断是否有制胜策略覆盖
    for action in actions:
        print("738动作名称\n", action["action_name"])
        it_mum = 1
        e = 1
        timeout = time.time()+10
        while (time.time() < timeout):
            # print(ConcreteExs)\
            last_e = e
            if(Enumerate_algorithm(it_mum, 'Int') == False):
                break  # 枚举超时，换动作
            e = Enumerate_algorithm(it_mum, 'Int')
            e = e[0]  # z3表达式[x,x] 一个
            # print("枚举的结果", e)
            if(type(e) == type(X)):
                e = simplify(e)

            s = Solver()
            if (str(e) != str(last_e)):
                action_temp = copy.deepcopy(action)
                if (str(action_temp).find("k") != -1):  # 用枚举得int代替action中的K_num
                    action_temp = eval(
                        str(action_temp).replace("k", '('+str(e)+')'))
                    # print("766",e)
                # This is the constrains of this cover
                # s.add(Game["Constraint"])  # 定义7
                s.add(Not(Implies(And(cover, Game["Constraint"]), And(action_temp["precondition"], ForAll(
                    [Y, Y1], Implies(action_temp["transition_formula"], Not(Winning_formula_Y())))))))
                # print(s.check())

                if (s.check() == unsat):
                    Winning_strategy.append(
                        [cover, action["action_name"]+"("+str(e)+")"])
                    # print("find")
                    print('919这是一个成功得块', cover,
                          action["action_name"]+"("+str(e)+")")
                    flag_strategy = True
                    break

                else:
                    m = s.model()  # model模型解
                    # print('774模型解:',m)
                    num1 = m[X].as_long()
                    if(Game["var_num"] == 2):
                        num2 = m[X1].as_long()
                    s_tem = Solver()
                    s_tem.add(cover)
                    s_tem.add(X == num1)
                    if (Game["var_num"] == 2):
                        s_tem.add(X1 == num2)
                    if(s_tem.check() != sat):
                        if (Game["var_num"] == 1):
                            num1 = findnum_strategy(
                                cover, ConcreteExs, Game["Constraint"])
                        if (Game["var_num"] == 2):
                            num1, num2 = findnum_strategy(
                                cover, ConcreteExs, Game["Constraint"])
                            # print("785找新的num值：", num1, "  ", num2)
                    if (Game["var_num"] == 1):
                        if(f_strategy(action["precondition"], action["transition_formula"], Game["Constraint"], num1) == "no suitable k"):
                            print("943没有枚举到符合条件得k值")
                            break
                    if (Game["var_num"] == 2):
                        if(f_strategy(action["precondition"], action["transition_formula"], Game["Constraint"], num1,num2) == "no suitable k"):
                            print("943没有枚举到符合条件得k值")
                        break
                    if (Game["var_num"] == 1):
                        result = f_strategy(action["precondition"], action["transition_formula"], Game["Constraint"], num1)
                    if (Game["var_num"] == 2):
                        result = f_strategy(action["precondition"], action["transition_formula"], Game["Constraint"], num1, num2)
            else:
                # print('two expresion equal')
                # 草率了，这里需要判断是否只有num1
                if(f_strategy(action["precondition"], action["transition_formula"], Game["Constraint"], num1, num2) == "no suitable k"):
                    print("951没有枚举到符合条件得k值")
                    break
                if(Game["var_num"] == 1):
                    num1 = findnum_strategy(
                        cover, ConcreteExs, Game["Constraint"])  # 满足条件且不在反例集和中的
                if(Game["var_num"] == 2):
                    num1, num2 = findnum_strategy(
                        cover, ConcreteExs, Game["Constraint"])
                   # print(num1, num2)
                result = f_strategy(
                    action["precondition"], action["transition_formula"], Game["Constraint"], num1, num2)
                s = Solver()
                s.add(Game["Constraint"])  # 定义7
                s.add(Not(Implies(And(cover, Game["Constraint"]), And(action_temp["precondition"],
                                                                      ForAll([Y, Y1], Implies(action_temp["transition_formula"], Not(Winning_formula_Y())))))))
                # print()
                # print(s.check())

                if (s.check() == unsat):
                    Winning_strategy.append(
                        [cover, action["action_name"]+"("+str(e)+")"])
                    # print("find")
                    print('973这是一个成功得块', cover,
                          action["action_name"]+"("+str(e)+")")
                    flag_strategy = True
                    break
            if (Game["var_num"] == 1):
                if ({'Input': {c: num1}, 'Output': result}) not in ConcreteExs:
                    ConcreteExs.append(
                        {'Input': {c: num1}, 'Output': result})
                    goal['value'].append(result)
                    it_mum = it_mum + 1
            if(Game["var_num"] == 2):  # 跟新ConcreteExs
                if ({'Input': {c: num1, d: num2}, 'Output': result}) not in ConcreteExs:
                    ConcreteExs.append(
                        {'Input': {c: num1, d: num2}, 'Output': result})
                    goal['value'].append(result)
                    it_mum = it_mum + 1
    if flag_strategy == False:
        print("#需要对该块进行细分，并将分好的快添加到refinement中：")
        # for action in actions:
        #     ConcreteExs.clear()
        #     goal={'value':[],'type':''}
        #     goal['type']='Bool'
        # flag=条件表达式含v1 v2的数量
        flag_exp = [['X1>X', 'X==X1'], ["X1>X+2", "X1==X+1", "X1<X+2"]]
        #     #拆分condition
        # strConstraint=str(Game["Constraint"])
        # strConstraint.split() #划分出右 v1 v2 的表达式
        # for action in actions:
        #     it_num =1
        #     e=-1;
        #     # while(True):#枚举bool表达式满足cover
        #     refinement.append(cover+"")
        # 先根据约约束条件进行划分，再根据动作的条件进行划分
        # 排除那些是终端条件的动作
        # 直接看cover的大小来决定连接那个表达式
        # print(cover)
        for i in flag_exp[len(str(cover)) - len((str(cover).replace(",", "")))]:
            # print(i)
            if("And" in str(cover)):
                refinement.append(str(cover)[:str(cover).rfind(")")]+","+i+")")
            else:
                refinement.append("And"+"("+str(cover)+","+i+")")

        # refinement.append(eval(''))


# ---------------------------------------------------------------------------------------------
total_time_use = (time.time() - start_total)
print("------------------------------------------------------------------------------------------------")
# print("winning strategy:", Winning_strategy)
print("Winning_strategy:")
for i in Winning_strategy:
    print(i)
# print("Winning strategy Time used:",total_time_use-refine_time_used-generate_winning_formula_time)
print("Total Time used:", total_time_use)
