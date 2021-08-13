def refinementPath(pathFormula):
    ans = [] #一个或多个 
    str1 = str(pathFormula)
    str1 = str1.replace(' ', '')
    arr1 = []
    if "And" in str1:
        str2 = str1[str1.rfind(",")+1:-1]
    else:
        str2 = str1
    print("2080",str2)
    if "Not" in str2: 
        str2 = str2[4:-1]
        if "%" in str2: # a%b==c
            b = str2[str2.find('%')+1:str2.find("==")]
            c = str2[str2.find("==")+2:]
            for i in range(0,eval(b)):
                if  str(i) != c:
                    arr1.append(str2[:str2.find("==")+2]+str(i))
        elif "==" in str2: #==
            arr1.append(str2.replace("==",">"))
            arr1.append(str2.replace("==","<"))
    else:
        if ">=" in str2:
            arr1.append(str2.replace(">=",">"))
            arr1.append(str2.replace(">=","=="))
        elif "<=" in str2:
            arr1.append(str2.replace("<=","<"))
            arr1.append(str2.replace("<=","==")) 
    if arr1 == []:
        arr1.append(str2)
    for f in arr1:
        if "And" in str1:
            ans.append(str1.replace(str1[str1.rfind(",")+1:],f)+")")
        else:
            ans.append(f)
    # print("refinement path :",ans)
    return ans

str1 = "And(Not(X%9 == 0),Not(X%9 == 2),Not(X + X == 8),Not(X + 8 == 14))"
arr1 = refinementPath(str1)
print(arr1)