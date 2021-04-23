from typing import List


class Solution:
    def verifyPostorder(self, postorder: List[int]) -> bool:
        #二叉搜索树 右》中》左
        if len(postorder)==1 or len(postorder)==0: return True
        a=postorder.pop()
        print(a)
        minorder,maxorder=postorder,[] 
        for i in range(len(postorder)):
            if postorder[i]>a:#比我大才划分，没有比我大的呢
                minorder=postorder[:i]
                maxorder=postorder[i:]
                # print(minorder)
                # print(maxorder)
                break
        if len(maxorder)!=0:
            for i in maxorder:
                if i<a :return False
        return self.verifyPostorder(minorder) and self.verifyPostorder(maxorder) 

s=Solution()
print(s.verifyPostorder([5, 2, -17, -11, 25, 76, 62, 98, 92, 61]))
