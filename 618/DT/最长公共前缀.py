from typing import List

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        ans = ""
        flag=1
        if len(strs) == 0: return ""
        if len(strs[0])==0 : return ""
        
        for i in range(1,len(strs[0])+1) :  
            #利用第一个字符串的长度进行遍历 切片左闭右开
            str = strs[0][:i]
            #对于列表的所有的字符串都前缀相等
            for j in strs[1:]:
                if str != j[:i]: 
                   return ans
            ans = str
        return ans

s= Solution
strs = ["asd"]
str = s().longestCommonPrefix(strs)
print(str)


# str = 'qwesswq'
# str1= str[1:1]
# print(str1)


