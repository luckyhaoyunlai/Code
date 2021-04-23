   for num in range(ptsLength):
        if(Goal[num] == ptsGoal[num]):  # 跟新cover[term]
            if term not in cover:
                cover[term] = []
            if pts[num] not in cover[term]:
                cover[term].append(pts[num])
    # 判断cover[term]是否重复了,先判断term是否在cover中
    if term in cover and term not in terms:  # 更新terms
        flag = False
        for t in cover:
            if(str(t) != str(term) and cover[t] == cover[term]):
                flag = True
                break
        if(flag == False):
            return term