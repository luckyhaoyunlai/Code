
def extractNum(str):
    str = str.replace(" ",'')
    ans = []
    i = 0 
    while i<len(str):
        if str[i]<='9' and str[i]>="0":
            ch = str[i]
            while(i<len(str)-1 and str[i+1]<='9' and str[i+1]>='0'):
                i = i+1
                ch = ch +str[i]
            ans.append(eval(ch))
        i +=1
    return ans
    
str = "And(1x3>15,y>9,x%10==1)"
arr = extractNum(str)
print(arr)