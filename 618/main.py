import os

PDDLdirectory='pddl1\Subtraction_game\TwoValue' 
PDDLlist = os.listdir(PDDLdirectory)
PDDLlist = sorted(PDDLlist,key=lambda x: os.path.getmtime(os.path.join(PDDLdirectory, x)))
for i in PDDLlist:
    if 'pddl' in i:
        print(i)
        i=PDDLdirectory+'\\'+i
        os.system("python DTsolver.py %s" %i)