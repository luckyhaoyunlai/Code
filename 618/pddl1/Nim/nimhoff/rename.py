import os
path = './'
fileList=os.listdir(path)
print(fileList)


testStr = 'a-rowed Chomp Game(v3  1))'
def spaceToHyphen(str):
    s = list(str) 
    for i in range (0,len(s)):
        if s[i] == ' ':
            s[i] = '-'
    s = ''.join(s)
    return s
def titleCase(str):
    s = list(str) 
    # if ord(s[0]) > 96 & ord(s[0]) < 123 :
    #     s[0] = chr(ord(s[0]) - 32)   
    s[0] = 'N'
    s = ''.join(s)
    print(s)
    return s
    
for i in fileList:
    oldname=path+ os.sep + i
    tempname=titleCase(i)
    newname= path+ os.sep + tempname
    os.rename(oldname,newname)

