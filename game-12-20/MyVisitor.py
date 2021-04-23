from subfile.PDDLGrammarVisitor import PDDLGrammarVisitor
from subfile.PDDLGrammarParser import PDDLGrammarParser
from z3 import *

parameter_list = []
action_list = []
effectList = []
object_list = []
obj_two = []
obj_all = []

class CEffect:

    def __init__(self):
        self.gd = Bool('gd')
        self.pEffectList = []

class Effect:
    def __init__(self):
        self.cEffectList = []

class Effect:
    def __init__(self):
        self.cEffectList = []
        self.formula = Bool('formula')


class PEffect:
    def __init__(self):
        self.assignop = ''
        self.var = Int('Var')
        self.var2 = Int('Var2')
        self.term = Int('term')


class Action:
    def __init__(self):
        self.name=''
        self.precondition=Bool('precondition')
        self.effect=Bool('effect')


class Item:
    def __init__(self):
        self.domain_name = ''
        # l.append(self.domain_name)
        self.objects = []
        self.type = ''
        self.action_list = []
        self.tercondition = Bool('tercondition')


game = Item()

class MyVisitor(PDDLGrammarVisitor):

    def __init__(self):
        self.memory = {}
   
    def visitListVariable(self, ctx):
        return [ctx.VAR(i).getText() for i in range(len(ctx.VAR()))]

    def visitAnd(self,ctx):
        return And([self.visit(ctx.gd(i)) for i in range(len(ctx.gd()))])


    def visitOr(self,ctx):
        return Or([self.visit(ctx.gd(i)) for i in range(len(ctx.gd()))])


    def visitIsGd(self,ctx):
        return self.visit(ctx.gd())

    def visitConstraintDefine(self, ctx):
        constraint = self.visit(ctx.emptyOrPreGD())
        print("Constraint:",constraint)
     
    def visitActionDefine(self, ctx):
        action = Action()
        action.name = ctx.actionSymbol().getText()
        print("Action Name:",action.name)
        action.precondition = self.visit(ctx.emptyOrPreGD())
        print("Precondition:",action.precondition)
        firstEffect = self.visit(ctx.emptyOrEffect())


        # Formula 2

        e = Int(str(effectList[0][1]) + '\'')
        if effectList[0][0]==True:
            FinalEffect = e == effectList[0][2]
        else:
            d = Int(str(effectList[0][1]) + '\'')
            # FinalEffect = e == effectList[0][2]
            FinalEffect = And(effectList[0][0], d == effectList[0][2])
        ff = 0
        # 初始版本
        for i in effectList:
            # print("i:",i)
            if ff == 0:
                ff = 1
                continue

            if i[0] == True:
                e = Int(str(i[1]) + '\'')
                FinalEffect = And(FinalEffect, e==i[2])

            else:
                if len(effectList) > 1:
                    # print("apple")
                    # print("saiojdioaj:",i[0])
                    d = Int(str(i[1]) + '\'')
                    FinalEffect = And(FinalEffect, i[0], d == i[2])

        j = 1
        flag = 0
        for i in effectList:

            if i[0] == True:
                continue
            else:
                if j == 1:
                    flag = 1
                    a = str(i[1]) + '\'' + ' == ' + str(i[1])
                    formu = Bool(a)
                    formula4 = Or(i[0], formu)
                    formula_3 = formula4
                    j = j + 1
                else:
                    flag = 1
                    j = j + 1
                    a = str(i[1]) + '\'' + '==' + str(i[1])
                    formu = Bool(a)
                    formula3 = Or(i[0],formu)
                    formula_3 = Or(formula3,formula_3)
                print("formula_3:", formula_3)

        # Formula 4

        sub_obj = []
        for i in object_list:
            sub_obj.append(i)

        print("effectList:",effectList)

        for i in effectList:
            for j in sub_obj:
                if str(i[1]) == j:
                    sub_obj.remove(j)
        # print("Formula 4中的sub_obj:",sub_obj)

        if len(sub_obj)>0:
            k=0
            for i in sub_obj:
                if k==0:
                    c = str(i + '\'' + ' == ' + i)
                    formula_4 = Bool(c)
                    k = k+1
                else:
                    c = str(i + '\'' + ' == ' + i)
                    formula_5 = Bool(c)
                    formula_4 = And(formula_4, formula_5)
            print("formula_4:", formula_4)

        transitionFormula = Bool('transitionFormula')
        if len(sub_obj)>0:
            if flag == 1:
                transitionFormula = And(action.precondition,FinalEffect, formula_3, formula_4)
            elif flag == 0:
                transitionFormula = And(action.precondition, FinalEffect, formula_4)
        else:
            if flag == 1:
                transitionFormula = And(action.precondition,FinalEffect, formula_3)
            elif flag == 0:
                transitionFormula = And(action.precondition, FinalEffect)

        print("Transition Formula:", transitionFormula)

        parameter_list = self.visit(ctx.listVariable())

        exist_list = []
        for i in parameter_list:
            exist_list.append(i[1:])

        final_list = []
        for i in range(0,len(exist_list)):
            s = Int(exist_list[i])
            final_list.append(s)
        return


    def visitIsEffect(self,ctx):
        return self.visit(ctx.effect())

    def visitAndCEffect(self, ctx):
        effectList.clear()
        for i in range(len(ctx.cEffect())):
            cEffect = self.visit(ctx.cEffect(i))
            effectList.append(cEffect)

        return effectList


    def visitCeffect(self, ctx):
        cEffect = self.visit(ctx.cEffect())
        effectList.clear()
        effectList.append(cEffect)


        return effectList


    def Effect(self, ctx):

        pEffect = PEffect()
        pEffect.assignop = self.visit(ctx.assignop())
        pEffect.var = Int(ctx.VAR().getText()[1:])
        pEffect.var2 = Int(ctx.VAR().getText()[1:] + '\'')
        pEffect.term = self.visit(ctx.term())


        if pEffect.assignop == 'decrease':
            return pEffect.var2 == pEffect.var - pEffect.term

        elif pEffect.assignop == 'increase':
            return pEffect.var2 == pEffect.var + pEffect.term

        else:
            return pEffect.var == pEffect.term


    def visitAndPEffect(self, ctx):
        pEffectList = []
        for i in range(len(ctx.pEffect())):
            pEffect = self.visit(ctx.pEffect(i))
            pEffectList.append(pEffect)
        return pEffectList

    def visitCondEffectPEffect(self, ctx):
        pef = self.visit(ctx.pEffect())
        var = Int(ctx.pEffect().VAR().getText()[1:])
        eff = self.visit(ctx.pEffect().term())
        return [var,eff]

    def visitWhenCondEffect(self, ctx):
        cEffect = CEffect()
        cEffect.gd = self.visit(ctx.gd())
        cEffect.condEffect=self.visit(ctx.condEffect())
        cEffect.pEffectList.append(self.visit(ctx.gd()))
        effList = cEffect.condEffect
        for i in effList:
            cEffect.pEffectList.append(i)   
        return cEffect.pEffectList


    def visitCEffectPEffect(self, ctx):
        var = Int(ctx.pEffect().VAR().getText()[1:])
        eff = self.visit(ctx.pEffect().term())
        return [True,var,eff]


    def visitEffectBracket(self, ctx):
        # effectList = []
        return Bool(True)

    # 【】【】【】
    def visitDec(self, ctx):
        if ctx.DEC():
            return ctx.DEC().getText()

    def visitAssign(self,ctx):
        if ctx.ASSIGN():
            return ctx.ASSIGN().getText()


    def visitPreGDBracket(self, ctx):
        return Bool(True)


    def visitGreaterThanEqual(self, ctx):
        value = ctx.getText()

        left = self.visit(ctx.term(0))
        right = self.visit(ctx.term(1))


        return left >= right

    # 【】【】【】
    def visitLessThanEqual(self, ctx):
        value = ctx.getText()
        left = self.visit(ctx.term(0))
        right = self.visit(ctx.term(1))
        return left <= right

    def visitLessThan(self, ctx):
        value = ctx.getText()
        left = self.visit(ctx.term(0))
        right = self.visit(ctx.term(1))
        return left < right


    def visitGreaterThan(self, ctx):
        left = self.visit(ctx.term(0))
        right = self.visit(ctx.term(1))
        return left > right


    # 【】【】【】
    def visitInteger(self,ctx):
        # value = ctx.getText()
        # print(value)
        return int(ctx.getText())

    # 【】【】【】
    def visitVar(self,ctx):
        value = ctx.getText()
        # print(type(value))
        # value = self.visit(ctx.VAR())
        # print(value)


        # 旧的成立的
        value_2 = Int(value[1:])
        # print("value："+value)

        # print("This is var:"+str(value_2))

        # value_2 = value[1:]
        return value_2

    def visitMinusTermTerm(self,ctx):
        left = self.visit(ctx.term(0))
        right = self.visit(ctx.term(1))
        return left - right

    def visitPlusTermTerm(self,ctx):
        left = self.visit(ctx.term(0))
        right = self.visit(ctx.term(1))
        return left + right

    def visitBracketTerm(self, ctx):
        value = ctx.getText()
        value_2 = Int(value[0:1]+value[2:])
        return value_2

    def visitModTermTerm(self, ctx):
        # value = ctx.getText()

        left = self.visit(ctx.term(0))
        right = self.visit(ctx.term(1))

        # value_2 = Int(value)
        # print("value2:"+value)

        return left%right



    # 【】【】【】
    def visitEqual(self,ctx):
        value = ctx.getText()

        left = self.visit(ctx.term(0))
        right = self.visit(ctx.term(1))

        return left == right


    # 【】【】【】
    def visitName(self, ctx):
        value = ctx.getText()
        # value = self.visit(ctx.term(0))
        # print("Name:", value)
        return value

    def visitObjectDefine(self, ctx):
        obj = self.visit(ctx.listVariable())
        for i in obj:
            i = i[1:]
            object_list.append(i)
        obj_two = object_list
        return object_list

    def visitTerconditionDefine(self, ctx):
        game.tercondition = self.visit(ctx.emptyOrPreGD())
        print("Terminal Condition:",game.tercondition)
        # print(game.tercondition)
        # return 0
