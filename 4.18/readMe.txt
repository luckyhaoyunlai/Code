打开PowerShell，切换到当前目录下
#前提准备 下载antlr-4.8-complete.jar到目录C:\Javalib
下载 antlr4 z3-solver

解析g4文件：
java -jar C:\Javalib\antlr-4.8-complete.jar -Dlanguage=Python3 PDDLGrammar.g4 -o subfile

生成遍历器：
java -jar C:\Javalib\antlr-4.8-complete.jar -Dlanguage=Python3 -no-listener -visitor PDDLGrammar.g4 -o subfile

解析命令：
python Init.py "pddl/Chomp_game.pddl"