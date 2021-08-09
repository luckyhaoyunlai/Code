

str1 = "And(x1>5,Not(x%31==0),Not(x3==2),Not(x2<4),x3>=7,Not(v1%7==8))"
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
