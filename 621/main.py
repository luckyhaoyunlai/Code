import os

PDDLdirectory='pddl1\chomp' 
PDDLlist = os.listdir(PDDLdirectory)
PDDLlist = sorted(PDDLlist,key=lambda x: os.path.getmtime(os.path.join(PDDLdirectory, x)))
resultFile="Result\Result_chomp.txt"
for i in PDDLlist:
    if 'pddl' in i:
        print(i)
        i=PDDLdirectory+'\\'+i
        os.system("python DTsolver.py %s %s" %(i,resultFile))