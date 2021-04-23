import sys
from antlr4 import *
from subfile.PDDLGrammarLexer import PDDLGrammarLexer
from subfile.PDDLGrammarParser import PDDLGrammarParser
from z3 import *
from MyVisitor import MyVisitor

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
        
    visitor = MyVisitor()
    visitor.visit(tree)
    
    