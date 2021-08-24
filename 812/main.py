import os

"""input PDDLdirectory and save result to resultFile"""
PDDLdirectory=r'pddl1\_Nim\_(2.1-2.3)\823' #执行文件夹
PDDLlist = os.listdir(PDDLdirectory)
PDDLlist = sorted(PDDLlist,key=lambda x: os.path.getmtime(os.path.join(PDDLdirectory, x)))
resultFile = r"C:\Users\admin\Desktop\test\result\test.xls" #结果位置
for i in PDDLlist:
    if 'pddl' in i:
        print(i)
        i=PDDLdirectory+'\\'+i
        # os.system("python DTsolver.py %s %s"%(i,resultFile))
        os.system("python DT+refinemnet.py %s %s"%(i,resultFile))




