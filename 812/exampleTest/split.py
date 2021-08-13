

str1 = "And(Not(X%9 == 0),Not(X%9 == 2),Not(X + X == 8),Not(X + 8 == 14))"
str1 = str1[4:-1]
print(str1)
arr = str1.split(",")
arr1 = []
print(arr)
for s in arr:
    if "Not" in s: 
        s = s[4:-1]
        print(s)
        if "%" in s: #%=
            a = s[:s.find('%')-1]
            b = s[s.find('%')+1:s.find("==")]
            c = s[s.find("==")+2:]
            for i in range(0,eval(b)):
                if  str(i) != c:
                    arr1.append(s.replace(c,str(i)))
        elif "==" in s: #==
            arr1.append(s.replace("==",">"))
            arr1.append(s.replace("==","<"))
    else:
        if ">=" in s:
            arr1.append(s.replace(">=",">"))
            arr1.append(s.replace(">=","=="))
        elif "<=" in s:
            arr1.append(s.replace("<=","<"))
            arr1.append(s.replace("<=","=="))
print(arr1)

str4 = "abc"
if "ab" in str4:
    print(str4.find('bc'))
    print("in有效")

str1 = "And(x1>5,Not(x3%7==1))"
str2 = "Not(x%31==0)"
str3 = "x>4"
str4 = "And(Not(X%9==0),Not(X%9==2),Not(X+X==8),Not(X+8==14))"
ans = []
str1 = str4
if "And" in str1:
    str2 = str1[str1.rfind(",")+1:-1]
else:
    str2 = str1
arr1 = []
if "Not" in str2: 
    str2 = str2[4:-1]
    if "%" in str2: #%=
        a = str2[:str2.find('%')-1]
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
    else :
        ans.append(f)
print(ans)
