import sys
from antlr4 import *
from subfile.PDDLGrammarLexer import PDDLGrammarLexer
from subfile.PDDLGrammarParser import PDDLGrammarParser
from z3 import *
from MyVisitor import MyVisitor
from MyVisitor import game
from z3 import *
import copy
import time
from opera import *
start_total=time.time()
X=Int('X')
Y=Int('Y')
X1=Int('X1')
Y1=Int('Y1')
k=Int('k')
print("==============================================================================")
if __name__ == '__main__':   #非导入的模块时 
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = InputStream(sys.stdin.readline()) #文件流
        
    lexer = PDDLGrammarLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = PDDLGrammarParser(token_stream)
    tree = parser.domain()
    s = Solver()  
    visitor = MyVisitor()#访问器对象  myvisitor继承了PDDLGrammarVisitor
    visitor.visit(tree) #visit()
print("==============================================================================")
# -----------------------------------------------------------
print("var_num:",game.objectsCount)
Terminal_Condition=eval(str(game.tercondition).replace('v1','X').replace('v2','X1'))
Constarint=eval(str(game.constraint).replace('v1','X').replace('v2','X1'))
actions=[]
for i in game.action_list:
    one={"action_name":i[0],
         "precondition":eval(str(i[1]).replace('v1','X').replace('v2','X1')),
         "transition_formula":eval(str(i[2]).replace('v1\'','Y').replace('v2\'','Y1').replace('v1','X').replace('v2','X1')) }
    actions.append(one)
#2-chomp-game
# print(actions)
# print(game.objectsCount)
# print(Terminal_Condition)
# print(Constarint)
# print("类型",game.type)
Game = {"Terminal_Condition":Terminal_Condition ,
        "actions": actions,
        "Constraint":Constarint,
        "var_num":game.objectsCount ,
        "type":game.type,
        "appeal_constants": []}   

NUMBER_CONSTANT = {1:"One",2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven",
                   8:"Eight", 9:"Nine"}

# The vocabulary that the enumrate algorithm used
vocabulary=[{'Input':['Int','Int'],'Output':'Int','Function_name':'Add','arity':2},
            {'Input': ['Int', 'Int'], 'Output': 'Int', 'Function_name': 'Sub','arity':2},
            {'Input': ['Int'], 'Output': 'Int', 'Function_name': 'Inc','arity':1},
            {'Input': ['Int'], 'Output': 'Int', 'Function_name': 'Dec','arity':1},
            {'Input': ['Int', 'Int'], 'Output': 'Bool', 'Function_name': 'Equal', 'arity': 2},
            {'Input': ['Int', 'Int'], 'Output': 'Bool', 'Function_name': 'Unequal', 'arity': 2},
            {'Input': ['Int','Int'], 'Output': 'Bool', 'Function_name': 'Ge','arity':2},
            {'Input': ['Int','Int'], 'Output': 'Bool', 'Function_name': 'Gt','arity':2},
            {'Input': ['Bool','Bool'], 'Output': 'Bool', 'Function_name': 'OR', 'arity': 2},
            {'Input': ['Bool','Bool'], 'Output': 'Bool', 'Function_name': 'AND', 'arity': 2},
            {'Input': [], 'Output': 'Int','Function_name': 'Zero', 'arity': 0},
            {'Input': [], 'Output': 'Int','Function_name': 'One', 'arity': 0},
            {'Input': ['Int','Int','Int'],'Output':'Bool','Function_name':'ModTest','arity':3}
]
for i in Game["appeal_constants"]:
    vocabulary.append({'Input': [], 'Output': 'Int','Function_name': NUMBER_CONSTANT[i], 'arity': 0},)

c=Int('c')
d=Int('d')
goal={'value':[],'type':''} #The goal that the enumerate algorithm generated
FunExg={'Add':Add,'Sub':Sub,'Inc':Inc,'Dec':Dec,'Ge':Ge,
        'Gt':Gt,'OR':OR,'AND':AND,'NOT':NOT,'Equal':Equal,'Mod':Mod,
        'Unequal':Unequal,'X':X,'Y':Y,'Zero':Zero,'One':One,'ModTest':ModTest}
if(Game["var_num"]==2):
    FunExg['X1']=X1
    FunExg['Y1'] = Y1
for i in Game["appeal_constants"]:
    FunExg[NUMBER_CONSTANT[i]]=eval(NUMBER_CONSTANT[i])
# z3 operator of FunExg
Z3FunExg={'Add':Add,'Sub':Sub,'Inc':Inc,'Dec':Dec,'Ge':Ge,
        'Gt':Gt,'OR':z3OR,'AND':z3AND,'NOT':z3NOT,'Equal':Equal,'Mod':Mod,
        'Unequal':Unequal,'X':X,'Y':Y,'Zero':Zero,'One':One,'ModTest':ModTest}
if(Game["var_num"]==2):
    Z3FunExg['X1']=X1
    Z3FunExg['Y1'] = Y1
for i in Game["appeal_constants"]:
    Z3FunExg[NUMBER_CONSTANT[i]]=eval(NUMBER_CONSTANT[i])


ConcreteExs=[]

start_winning_formula_time=time.time()

# The enumerative algorithm for multiple objects
def Enumerate_algorithm(count,Goal_type):
    goal['type'] = Goal_type
    SigSet = []
    ExpSet = []
    SizeOneExps = []

    SizeOneExps.append({'Input': ['Int'], 'Output': 'Int', 'Expression': 'X', 'z3Expression': [X,Y], 'arity': 1, 'size': 1})
    if(Game["var_num"]==2):
        SizeOneExps.append({'Input': ['Int'], 'Output': 'Int', 'Expression': 'X1', 'z3Expression': [X1,Y1], 'arity': 1, 'size': 1})
    SizeOneExps.append({'Input': [], 'Output': 'Int', 'Expression': 'Zero', 'z3Expression': [Zero(),Zero()], 'arity': 0, 'size': 1})
    SizeOneExps.append({'Input': [], 'Output': 'Int', 'Expression': 'One', 'z3Expression': [One(),One()], 'arity': 0,'size': 1})
    for i in Game["appeal_constants"]:
        SizeOneExps.append({'Input': [], 'Output': 'Int', 'Expression': NUMBER_CONSTANT[i], 'z3Expression': [eval(NUMBER_CONSTANT[i])(), eval(NUMBER_CONSTANT[i])()], 'arity': 0,'size': 1})

    for i in SizeOneExps:
        Goal1 = []
        if (i['arity'] == 0):
            for num in range(count):
                Goal1.append(FunExg[i['Expression']]())
            if Goal1 not in SigSet:
                SigSet.append(Goal1)
                i['Output_data'] = Goal1
                ExpSet.append(i)
                if Goal1 == goal['value'] and i['Output'] == goal['type']:
                    return i['z3Expression']
        else:
            if i['Expression'] == 'X':
                for j in ConcreteExs:
                    O = j['Input'][c]
                    Goal1.append(O)
                if Goal1 not in SigSet:
                    SigSet.append(Goal1)
                    i['Output_data'] = Goal1
                    ExpSet.append(i)
                    if Goal1 == goal['value'] and i['Output'] == goal['type']:
                        return i['z3Expression']
            if i['Expression'] == 'X1':
                for j in ConcreteExs:
                    O = j['Input'][d]
                    Goal1.append(O)
                if Goal1 not in SigSet:
                    SigSet.append(Goal1)
                    i['Output_data'] = Goal1
                    ExpSet.append(i)
                    if Goal1 == goal['value'] and i['Output'] == goal['type']:
                        return i['z3Expression']

    for i in vocabulary:
        if (i['arity'] == 1):
            for j in ExpSet:
                if j['size'] == 1:
                    Goal1 = []
                    if (i['Input'][0] == j['Output']):
                        TempExp = i['Function_name'] + '(' + j['Expression'] + ')'
                        z3TempExp1=Z3FunExg[i['Function_name']](j['z3Expression'][0])
                        z3TempExp2=Z3FunExg[i['Function_name']](j['z3Expression'][1])
                        for ki in j['Output_data']:
                            O = FunExg[i['Function_name']](ki)
                            Goal1.append(O)
                        if Goal1 not in SigSet:
                            SigSet.append(Goal1)
                            ExpSet.append(
                                {'Input': i['Input'], 'Output': i['Output'], 'Expression': TempExp,
                                 'z3Expression':[z3TempExp1,z3TempExp2],'arity': i['arity'],
                                 'size': 2, 'Output_data': Goal1})
                        if Goal1 == goal['value'] and i['Output'] == goal['type']:
                            return [z3TempExp1,z3TempExp2]
    i = 3
    while (True):
        for f in vocabulary:
            m = f['arity']
            if (m == 1):
                for j in ExpSet:
                    try:
                        Goal1 = []
                        if ((j['size'] == i - 1) and (f['Input'] == j['Output'])):
                            TempExp = f['Function_name'] + '(' + j['Expression'] + ')'
                            z3TempExp1 = Z3FunExg[f['Function_name']](j['z3Expression'][0])
                            z3TempExp2 = Z3FunExg[f['Function_name']](j['z3Expression'][1])
                            for ki in j['Output_data']:
                                O = FunExg[f['Function_name']](ki)
                                Goal1.append(O)
                            if Goal1 not in SigSet:
                                SigSet.append(Goal1)
                                ExpSet.append({'Input': f['Input'], 'Output': f['Output'],
                                               'Expression': TempExp,'z3Expression':[z3TempExp1,z3TempExp2],
                                               'arity': f['arity'], 'size': i, 'Output_data': Goal1})
                            if Goal1 == goal['value'] and f['Output'] == goal['type']:
                                return [z3TempExp1,z3TempExp2]
                    except ZeroDivisionError:
                        pass
                    continue
            elif (m == 2):
                for num1 in range(1, i - 1):
                    for num2 in range(1, i - 1):
                        if (num1 + num2 == i - 1):
                            for choose1 in ExpSet:
                                if (choose1['size'] == num1):
                                    for choose2 in ExpSet:
                                        if (choose2['size'] == num2):
                                            if ((f['Input'][0] == choose1['Output']) and (
                                                f['Input'][1] == choose2['Output'])):
                                                try:
                                                    Goal1 = []
                                                    TempExp = ''
                                                    TempExp = f['Function_name'] + '(' + choose1['Expression'] + ',' + choose2['Expression'] + ')'
                                                    z3TempExp1=Z3FunExg[f['Function_name']](choose1['z3Expression'][0],choose2['z3Expression'][0])
                                                    z3TempExp2=Z3FunExg[f['Function_name']](choose1['z3Expression'][1],choose2['z3Expression'][1])
                                                    for ki, h in zip(choose1['Output_data'], choose2['Output_data']):
                                                        O = FunExg[f['Function_name']](ki, h)
                                                        Goal1.append(O)
                                                    if Goal1 not in SigSet:
                                                        SigSet.append(Goal1)
                                                        ExpSet.append(
                                                            {'Input': f['Input'], 'Output': f['Output'],
                                                             'Expression': TempExp,'z3Expression':[z3TempExp1,z3TempExp2],
                                                             'arity': f['arity'], 'size': i, 'Output_data': Goal1})
                                                    # print(SigSet)
                                                    if Goal1 == goal['value'] and f['Output'] == goal['type']:
                                                        return [z3TempExp1,z3TempExp2]
                                                except ZeroDivisionError:
                                                    pass
                                                continue
            elif (m == 3):
                if (f['Function_name']=='ModTest'):
                    for num1 in range(1, i - 1):
                        for num2 in range(1, i - 1):
                            for num3 in range(1, i - 1):
                                if (num1 + num2 + num3 == i - 1):
                                    for choose1 in ExpSet:
                                        if (choose1['size'] == num1):
                                            for choose2 in ExpSet:
                                                if (choose2['size'] == num2):
                                                    for choose3 in ExpSet:
                                                        if (choose3['size'] == num3 and choose3['arity']==0):
                                                            if ((f['Input'][0] == choose1['Output']) and (f['Input'][1] == choose2['Output']) and (f['Input'][2] == choose3['Output'])):
                                                                try:
                                                                    Goal1 = []
                                                                    TempExp = ''
                                                                    TempExp = f['Function_name'] + '(' + choose1['Expression'] + ',' + choose2['Expression'] + ',' + choose3['Expression'] + ')'
                                                                    z3TempExp1 = Z3FunExg[f['Function_name']](choose1['z3Expression'][0],choose2['z3Expression'][0],choose3['z3Expression'][0])
                                                                    z3TempExp2 = Z3FunExg[f['Function_name']](choose1['z3Expression'][1],choose2['z3Expression'][1],choose3['z3Expression'][1])
                                                                    for ki, h, g in zip(choose1['Output_data'],choose2['Output_data'],choose3['Output_data']):
                                                                        O = FunExg[f['Function_name']](ki, h, g)
                                                                        Goal1.append(O)
                                                                    if Goal1 not in SigSet:
                                                                        SigSet.append(Goal1)
                                                                        ExpSet.append({'Input': f['Input'], 'Output': f['Output'],
                                                                                   'Expression': TempExp, 'z3Expression':[z3TempExp1,z3TempExp2],
                                                                                   'arity': f['arity'],'size': i, 'Output_data': Goal1})
                                                                    if Goal1 == goal['value'] and f['Output'] == goal['type']:
                                                                        return [z3TempExp1,z3TempExp2]
                                                                except ZeroDivisionError:
                                                                    pass
                                                                continue
                else:
                    for num1 in range(1, i - 1):
                        for num2 in range(1, i - 1):
                            for num3 in range(1, i - 1):
                                if (num1 + num2 + num3 == i - 1):
                                    for choose1 in ExpSet:
                                        if (choose1['size'] == num1):
                                            for choose2 in ExpSet:
                                                if (choose2['size'] == num2):
                                                    for choose3 in ExpSet:
                                                        if (choose3['size'] == num3):
                                                            if ((f['Input'][0] == choose1['Output']) and (f['Input'][1] == choose2['Output']) and (f['Input'][2] == choose3['Output'])):
                                                                try:
                                                                    Goal1 = []
                                                                    TempExp = ''
                                                                    TempExp = f['Function_name'] + '(' + choose1['Expression'] + ',' + choose2['Expression'] + ',' + choose3['Expression'] + ')'
                                                                    z3TempExp1 = Z3FunExg[f['Function_name']](choose1['z3Expression'][0],choose2['z3Expression'][0],choose3['z3Expression'][0])
                                                                    z3TempExp2 = Z3FunExg[f['Function_name']](choose1['z3Expression'][1],choose2['z3Expression'][1],choose3['z3Expression'][1])
                                                                    for ki, h, g in zip(choose1['Output_data'],choose2['Output_data'],choose3['Output_data']):
                                                                        O = FunExg[f['Function_name']](ki, h, g)
                                                                        Goal1.append(O)
                                                                    if Goal1 not in SigSet:
                                                                        SigSet.append(Goal1)
                                                                        ExpSet.append({'Input': f['Input'], 'Output': f['Output'],
                                                                                   'Expression': TempExp, 'z3Expression':[z3TempExp1,z3TempExp2],
                                                                                   'arity': f['arity'],'size': i, 'Output_data': Goal1})
                                                                    if Goal1 == goal['value'] and f['Output'] == goal['type']:
                                                                        return [z3TempExp1,z3TempExp2]
                                                                except ZeroDivisionError:
                                                                    pass
                                                                continue
        i=i+1



O=Bool('O')
num=1
num1=0
flag=1
e=1

# The global transition formula
global_transition_formula="Exists(k,Or("
for i in Game["actions"]:
    global_transition_formula=global_transition_formula+str(i["transition_formula"])+","
global_transition_formula=global_transition_formula+"))"
global_transition_formula=eval(global_transition_formula)


f_1=[]
for x in range(0, 100):
    f_1.append('illegal')

f_2=[]
for x in range(0, 100):
    f_2.append([])
    for y in range(0,100):
        f_2[x].append('illegal')


s=Solver()
s.add(Game["Terminal_Condition"])
s.check()
m=s.model()
if(Game["var_num"]==1):
    f_1[m[X].as_long()]=True
if(Game["var_num"]==2):
    f_2[m[X].as_long()][m[X1].as_long()] = True

# This function is an recursive algorithm that to find whether a state is a winning state or a losing state
def F(*v):
    if (len(v)==1):
        if (f_1[v[0]] != 'illegal'):
            return f_1[v[0]]
        for x in range(0, v[0] + 1):
            if (f_1[x] != 'illegal'):
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
                if (f_1[i[0]] == 'illegal'):
                    f_1[i[0]] = F(i[0])
            for i in temp:
                is_losing = is_losing and not f_1[i[0]]
            if (is_losing):
                f_1[x] = True
            else:
                f_1[x] = False
        return f_1[v[0]]

    if(len(v)==2):
        if(f_2[v[0]][v[1]]!='illegal'):
            return f_2[v[0]][v[1]]
        for x in range(0, v[0]+1):
            for y in range(0, v[1]+1):
                if(f_2[x][y]!='illegal'):
                    continue
                temp = []
                while (True):

                    s = Solver()
                    s.add(global_transition_formula)
                    s.add(Game["Constraint"])
                    s.add(X == x, X1 == y)
                    for i in temp:
                        s.add(Or(Y != i[0], Y1 != i[1]))
                    if (s.check() == sat):
                        m = s.model()
                        temp.append([m[Y].as_long(), m[Y1].as_long()])
                    else:
                        break
                is_losing = True
                s=Solver()
                s.add(Game["Constraint"])
                s.add(X==x,X1==y)
                if(s.check()==unsat):
                    continue
                for i in temp:
                    if(f_2[i[0]][i[1]]=='illegal'):
                        f_2[i[0]][i[1]]=F(i[0],i[1])
                for i in temp:
                    is_losing = is_losing and not f_2[i[0]][i[1]]
                if (is_losing):
                    f_2[x][y] = True
                else:
                    f_2[x][y] = False
        return f_2[v[0]][v[1]]

# This function aims to enumerate states in an increasing order of the sum of values
#  of all state variables until find a suitable state
def Findnum(ConcreteExs):
    if (Game["var_num"] == 1):
        i=2
        while(True):
            for v1 in range(0, i):
                flag12 = False
                for example in ConcreteExs:
                    if (v1 == example['Input'][c]):
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
    if(Game["var_num"]==2):
        i = 2
        while(True):
            for v1 in range(0,i):
                for v2 in range(0,i):
                    if v1+v2==i:
                        flag12 = False
                        for example in ConcreteExs:
                            if (v1==example['Input'][c] and v2==example['Input'][d]):
                                flag12=True
                        if flag12==False:
                            s=Solver()
                            s.add(Game["Constraint"])
                            s.add(X==v1,X1==v2)
                            if(s.check()==sat):
                                return v1,v2
                            else:
                                continue
            i=i+1 
        
# The following is the process of generating the winning formula
# This process will continue until  find the winning formula
# This process will generate the losing formula, and the winning formula is its negation
while(True):
    last_e=e
    e=Enumerate_algorithm(num,'Bool')
    print("枚举出候选的必败态：", e)
    print('反例集合', ConcreteExs)
    print("反例的数目",len(ConcreteExs))
    i = Int('i')
    i1=Int('i1')
    s = Solver()

    if(e!=last_e):
        # The following are the constraints for the winning formula
        # s.set('timeout',6000)
        #拆分去比较 如果终态--P--N--分别加入比较
        s.add(Or(And(Game["Terminal_Condition"], Not(e[0])),
                    Not(Implies(And(e[0],Game["Constraint"]), ForAll([Y, Y1], Implies(global_transition_formula, Not(e[1]))))),
                    Not(Implies(And(Not(e[0]),Game["Constraint"]), Exists([Y, Y1], And(global_transition_formula, e[1]))))))
    # print(s.check())
        if(s.check()==unsat):
                losing_formula=e[0]
                losing_formula_Y=e[1]
                print("The Winning formula of this game is:",Not(losing_formula))
                generate_winning_formula_time = (time.time() - start_winning_formula_time)
                print("Time to generate the winning formula:", generate_winning_formula_time)
                break
        # elif(s.check()==unknown):
        #     if(Game["var_num"]==1):
        #         while True:
        #             num4 = Findnum(ConcreteExs)
        #             if F(num4)=='illegal':
        #                 continue
        #             else:
        #                 break
        #     if(Game["var_num"]==2):
        #         while True:
        #             num4, num5 = Findnum(ConcreteExs)
        #             if F(num4,num5)=='illegal':
        #                 continue
        #             else:
        #                 break
        #elif(s.check()==sat):
        else:
            m=s.model()
            if (Game["var_num"] == 1):
                num4 = m[X].as_long()
                if F(num4) == 'illegal':
                    while True:
                        num4 = Findnum(ConcreteExs)
                        if F(num4)=='illegal':
                            continue
                        else:
                            break
            if (Game["var_num"] == 2):
                num4 = m[X].as_long()
                num5 = m[X1].as_long()
                if F(num4,num5) == 'illegal':
                    while True:
                        num4, num5 = Findnum(ConcreteExs)
                        print("找到的反例：",num4,num5)
                        if F(num4,num5)=='illegal':
                            print("怎么会有这一步呢")
                            continue
                        else:
                            break
    else:
        # When the the state s is not suitable to improve the candidate
        # Use the function Findnum to find an suitable state
        while True:
            if (Game["var_num"] == 1):
                num4 = Findnum(ConcreteExs)
                if F(num4) == 'illegal':
                    continue
                else:
                    break
            if (Game["var_num"] == 2):
                num4, num5 = Findnum(ConcreteExs)
                print("找到的反例：",num4,num5)
                if F(num4,num5) == 'illegal':#非法位置
                    print(num4,num5,"非法位置")
                    continue
                else:
                    break
    # Add the counterexample to ConcreteExs
    if (Game["var_num"] == 1):
        if ({'Input':{c:num4},'Output':F(num4)}) not in ConcreteExs:
            ConcreteExs.append({'Input':{c:num4},'Output':F(num4)})
            goal['value'].append(F(num4))
            num = num + 1
    if (Game["var_num"] == 2):
        if ({'Input':{c:num4,d:num5},'Output':F(num4,num5)}) not in ConcreteExs:
            ConcreteExs.append({'Input':{c:num4,d:num5},'Output':F(num4,num5)})
            goal['value'].append(F(num4,num5))
            num = num + 1
# ------------------------------------------------------------------



def Losing_formula():
    return losing_formula
def Winning_formula():
    return Not(losing_formula)
def Losing_formula_Y():
    return losing_formula_Y
def Winning_formula_Y():
    return Not(losing_formula_Y)

start_refine=time.time()

# The following function aim to refine the winning formula, it will return the covers of winning formula
def refine_the_winning_formula(Losing_formula):
    C=str(Losing_formula)
    C=C.replace(' ','')
    Ct = []
    if (C.find('And') == -1 and C.find('Or') == -1):
        if (C.find('==') != -1 and (type(eval(C[(C.find('==') + 2):])) == type(1)) and C.find('%') == -1):
            Ct = []
            Ct.append(C.replace('==', '<'))
            Ct.append(C.replace('==', '>'))
        elif (C.find('==') != -1 and (type(eval(C[(C.find('==') + 2):])) == type(X)) and C.find('%') == -1):
            Ct = []
            Ct.append(C.replace('==', '<'))
            Ct.append(C.replace('==', '>'))
        elif (C.find('%') != -1 and (type(eval(C[(C.find('==') + 2):])) == type(1))):
            Ct = []
            num = eval(C[(C.find('%') + 1):C.find('==')]) - 1
            # print(num)
            num_original = eval(C[(C.find('==') + 2):])
            while (num >= 0):
                if (num != num_original):
                    C = C[:C.find('==') + 2]
                    C = C + str(num)
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
                        Ct.append(C[C.find('X'):C.find(',')].replace(C[C.find('==') + 2], str(num)))
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
    return refinement,refine_time_used

# This function is an recursive algorithm that to find the corresponding action parameter of a state
def f_strategy(action_precondition,action_transition_formula,action_constraint,*v):
    s=Solver()
    s.add(Not(Winning_formula_Y()))
    s.add(action_precondition)
    s.add(action_transition_formula)
    s.add(action_constraint)
    s.add(X==v[0])
    if(Game["var_num"]==2):
        s.add(X1==v[1])
    if(s.check()==sat):
        m=s.model()
        return m[k].as_long()
    else:
        return "no suitable k"

# This function aims to enumerate states in an increasing order of the sum of values
#  of all state variables until find a suitable state
def findnum_strategy(cover,ConcreteExs,action_constraint):
    s=Solver()
    s.add(cover)
    s.add(action_constraint)
    if(Game["var_num"]==1):
        for i in ConcreteExs:
            s.add(Or(X!=i['Input'][c]))
    if(Game["var_num"]==2):
        for i in ConcreteExs:
            s.add(Or(X!=i['Input'][c],X1!=i['Input'][d]))
    s.check()
    m=s.model()
    if(Game["var_num"]==1):
        return m[X].as_long()
    if (Game["var_num"] == 2):
        return m[X].as_long(),m[X1].as_long()


Winning_strategy=[]
refinement,refine_time_used=refine_the_winning_formula(Losing_formula())

# The following is the process of generating the winning strategy for every covers of winning formula
# This process will choose the corresponding action and action parameter of every cover
for cover in refinement:
    # print("cover:",cover)
    s=Solver()
    s.add(cover)
    s.add(Game["Constraint"])
    if(s.check()==unsat):
        continue

    # The type of the initial search target is int
    ConcreteExs.clear()
    goal = {'value': [], 'type': ''}
    goal['type'] = 'Int'
    for action in actions:
        # print(action)
        it_mum = 1
        e = 1
        while (True):
            # print(ConcreteExs)
            last_e = e
            # print("expression_searching......")
            e = Enumerate_algorithm(it_mum,'Int')
            e=e[0]
            # print("expression_search_done")
            if(type(e)==type(X)):
                e=simplify(e)

            s = Solver()
            if (str(e) != str(last_e)):
                action_temp=copy.deepcopy(action)
                if (str(action_temp).find("k") != -1):
                    action_temp = eval(str(action_temp).replace("k", '('+str(e)+')'))

                # This is the constrains of this cover
                s.add(Game["Constraint"])
                s.add(Not(Implies(And(cover,Game["Constraint"]),And(action_temp["precondition"],
                 ForAll([Y,Y1],Implies(action_temp["transition_formula"],Not(Winning_formula_Y())))))))
                # print(s.check())
                if (s.check() == unsat):
                    Winning_strategy.append([cover,action["action_name"]+"("+str(e)+")"])
                    # print("find")
                    # print(Winning_strategy)
                    break
                else:
                    m = s.model()
                    # print(m)
                    num1=0
                    num2=0
                    num1 = m[X].as_long()
                    if(Game["var_num"]==2):
                        num2 = m[X1].as_long()
                    s_tem=Solver()
                    s_tem.add(cover)
                    s_tem.add(X==num1)
                    if (Game["var_num"] == 2):
                        s_tem.add(X1==num2)
                    if(s_tem.check()!=sat):
                        if (Game["var_num"] == 1):
                            num1 = findnum_strategy(cover, ConcreteExs, Game["Constraint"])
                        if (Game["var_num"] == 2):
                            num1, num2 = findnum_strategy(cover, ConcreteExs, Game["Constraint"])
                    if(f_strategy(action["precondition"], action["transition_formula"], Game["Constraint"],num1,num2)=="no suitable k"):
                        # print("no suitable k")
                        break
                    result = f_strategy(action["precondition"], action["transition_formula"], Game["Constraint"],num1,num2)
            else:
                print('two expresion equal')
                if(f_strategy(action["precondition"], action["transition_formula"],Game["Constraint"],num1, num2) == "no suitable k"):
                    # print("no suitable k")
                    break
                if(Game["var_num"]==1):
                    num1= findnum_strategy(cover, ConcreteExs, Game["Constraint"])
                if(Game["var_num"]==2):
                    num1,num2=findnum_strategy(cover,ConcreteExs,Game["Constraint"])
                result=f_strategy(action["precondition"],action["transition_formula"],Game["Constraint"],num1,num2)
            if (Game["var_num"] == 1):
                if ({'Input': {c: num1}, 'Output': result}) not in ConcreteExs:
                    ConcreteExs.append({'Input': {c: num1}, 'Output': result})
                    goal['value'].append(result)
                    it_mum = it_mum + 1
            if(Game["var_num"]==2):
                if ({'Input': {c: num1, d:num2}, 'Output': result}) not in ConcreteExs:
                    ConcreteExs.append({'Input': {c: num1, d:num2}, 'Output': result})
                    goal['value'].append(result)
                    it_mum = it_mum + 1

# ---------------------------------------------------------------------------------------------
total_time_use = (time.time() - start_total)
print("------------------------------------------------------------------------------------------------")
print("winning strategy:",Winning_strategy)
# for i in Winning_strategy:
#     print(i)
print("Winning strategy Time used:",total_time_use-refine_time_used-generate_winning_formula_time)
print("Total Time used:",total_time_use)