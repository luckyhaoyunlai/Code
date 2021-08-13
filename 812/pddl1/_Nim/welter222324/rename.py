import os
path = './'
fileList=os.listdir(path)
print(fileList)

testStr = '3-rowed Chomp Game(v3  1))'
def spaceToHyphen(str):

    s = list(str) 
    for i in range (0,len(s)):
        if s[i] == ' ':
            s[i] = '-'
    s = ''.join(s)
    return s
for i in fileList:
    oldname=path+ os.sep + i
    tempname=spaceToHyphen(i)
    newname= path+ os.sep + tempname
    os.rename(oldname,newname)
