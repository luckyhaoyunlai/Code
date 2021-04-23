def nextDistinctTerm(pts, cover, ptsGoal, terms):
    ptsLength = len(pts)
    if ptsLength == 0:
        return
    ExpSet = []  # 一轮枚举中枚举的term都但在这里，之后对这个进行运算，枚举更大的term
    SigSet = []
    sizeOneExps = []
    sizeOneExps.append({'Expression': 0, 'arity': 0, 'size': 1})
    sizeOneExps.append({'Expression': 1, 'arity': 0, 'size': 1})
    sizeOneExps.append({'Expression': X, 'arity': 1, 'size': 1})
    sizeOneExps.append({'Expression': Y, 'arity': 1, 'size': 1})
    # 怎么修剪枚举term，怎么设置成已经枚举过了哪个term,还是每次加入pt时都要重新枚举一遍
    # 枚举term
    for i in sizeOneExps:
        if(i['arity'] == 0):  # 枚举 0和1 不需要计算出k
            Goal = []
            term = i['Expression']  # term是取值'Zero'
            for num in range(ptsLength):
                Goal.append(i['Expression'])
            if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                SigSet.append(Goal)
                i['outputData'] = Goal
                ExpSet.append(i)
                # Goal和ptsGoal的匹配 从0匹配到最后一个 求cover[term]
                if term not in terms and term not in cover:
                    for num in range(ptsLength):
                        if(Goal[num] == ptsGoal[num]):
                            if term not in cover:
                                cover[term] = []
                            if pts[num] not in cover[term]:  # 不能重复把点输入cover中
                                cover[term].append(pts[num])
                    # 判断0.1不需要判断cover[term]是否重复了
                    if term in cover:
                        flag = False
                        for t in cover:
                            if(str(t) != str(term) and cover[t] == cover[term]):
                                flag = True
                                break
                        if(flag == False):
                            return term
        else:
            if i['Expression'] == X:
                Goal = []
                term = X
                for pt in pts:
                    Goal.append(pt[c])
                if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                    SigSet.append(Goal)
                    i['outputData'] = Goal
                    ExpSet.append(i)
                    # Goal和ptsGoal的匹配 从0匹配到最后一个 求cover[term]
                    for num in range(ptsLength):
                        if(Goal[num] == ptsGoal[num]):
                            if term not in cover:
                                cover[term] = []
                            if pts[num] not in cover[term]:  # 跟新cover[term]中
                                cover[term].append(pts[num])
                    # 判断cover[term]是否重复了
                    if term in cover and term not in terms:  # 跟新terms
                        flag = False
                        for t in cover:
                            if(str(t) != str(term) and cover[t] == cover[term]):
                                flag = True
                                break
                        if flag == False:
                            return term
            if i['Expression'] == Y:
                Goal = []
                term = Y
                for pt in pts:
                    Goal.append(pt[d])
                if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                    SigSet.append(Goal)
                    i['outputData'] = Goal
                    ExpSet.append(i)
                    # Goal和ptsGoal的匹配 从0匹配到最后一个 求cover[term]
                    for num in range(ptsLength):
                        if(Goal[num] == ptsGoal[num]):
                            if term not in cover:
                                cover[term] = []
                            if pts[num] not in cover[term]:  # 不能重复把点输入cover中
                                cover[term].append(pts[num])
                        # 判断cover[term]是否重复了
                    if term in cover and term not in terms:
                        flag = False
                        for t in cover:
                            if(str(t) != str(term) and cover[t] == cover[term]):
                                flag = True
                                break
                        if(flag == False):
                            return term
    # 上面0 1 ｘ　ｙ已经枚举完了　接下来按大小枚举更大的
    # 设计下自己枚举顺序 先所有的++
    MaxSize = 2
    while(True):
        # 严格按大小枚举term
        # 单纯时term的化是不是不需要t_vocabulary集合
        # 执行add sub 如果还要添加其他的操作再加入vocabulary
        for i in t_vocabulary:
            for size1 in range(1, MaxSize):
                for choose1 in ExpSet:
                    if(choose1['size'] == size1):
                        for choose2 in ExpSet:
                            if(choose2['size'] == MaxSize-size1):
                                term = FunExg[i['Function_name']](
                                    choose1['Expression'], choose2['Expression'])
                                Goal = []  # 计算goal
                                for k, h in zip(choose1['outputData'], choose2['outputData']):
                                    Goal.append(
                                        FunExg[i['Function_name']](k, h))
                                if Goal not in SigSet:  # 更新SigSet ExgSet
                                    SigSet.append(Goal)
                                    i['outputData'] = Goal
                                    ExpSet.append(
                                        {'Expression': term, 'arity': i['arity'], 'outputData': Goal, 'size': MaxSize})
                                    if term not in terms:
                                        # term不在terms才更新cover,且要求最后一个pt必须满足term
                                        for num in range(ptsLength):
                                            if(Goal[num] == ptsGoal[num]):  # 跟新cover[term]
                                                if term not in cover:
                                                    cover[term] = []
                                                if pts[num] not in cover[term]:
                                                    cover[term].append(
                                                        pts[num])
                                        # 判断cover[term]是否重复了,先判断term是否在cover中
                                        if term in cover and term not in terms:  # 更新terms
                                            flag = False
                                            for t in cover:
                                                if(str(t) != str(term) and cover[t] == cover[term]):
                                                    flag = True
                                                    break
                                            if(flag == False):
                                                return term
        MaxSize += 1


def nextDistinctTerm(pts, cover, ptsGoal, terms):
    ptsLength = len(pts)
    if ptsLength == 0:
        return
    ExpSet = []  # 一轮枚举中枚举的term都但在这里，之后对这个进行运算，枚举更大的term
    SigSet = []
    sizeOneExps = []
    sizeOneExps.append({'Expression': 0, 'arity': 0, 'size': 1})
    sizeOneExps.append({'Expression': 1, 'arity': 0, 'size': 1})
    sizeOneExps.append({'Expression': X, 'arity': 1, 'size': 1})
    sizeOneExps.append({'Expression': Y, 'arity': 1, 'size': 1})
    # 怎么修剪枚举term，怎么设置成已经枚举过了哪个term,还是每次加入pt时都要重新枚举一遍
    # 枚举term
    for i in sizeOneExps:
        if(i['arity'] == 0):  # 枚举 0和1 不需要计算出k
            Goal = []
            term = i['Expression']  # term是取值'Zero'
            for num in range(ptsLength):
                Goal.append(i['Expression'])
            if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                SigSet.append(Goal)
                i['outputData'] = Goal
                ExpSet.append(i)
                # Goal和ptsGoal的匹配 从0匹配到最后一个 求cover[term]
                if term not in terms and term not in cover:
                    for num in range(ptsLength):
                        if(Goal[num] == ptsGoal[num]):
                            if term not in cover:
                                cover[term] = []
                            if pts[num] not in cover[term]:  # 不能重复把点输入cover中
                                cover[term].append(pts[num])
                    # 判断0.1不需要判断cover[term]是否重复了
                    if term in cover:
                        flag = False
                        for t in cover:
                            if(str(t) != str(term) and cover[t] == cover[term]):
                                flag = True
                                break
                        if(flag == False):
                            return term
        else:
            if i['Expression'] == X:
                Goal = []
                term = X
                for pt in pts:
                    Goal.append(pt[c])
                if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                    SigSet.append(Goal)
                    i['outputData'] = Goal
                    ExpSet.append(i)
                    # Goal和ptsGoal的匹配 从0匹配到最后一个 求cover[term]
                    for num in range(ptsLength):
                        if(Goal[num] == ptsGoal[num]):
                            if term not in cover:
                                cover[term] = []
                            if pts[num] not in cover[term]:  # 跟新cover[term]中
                                cover[term].append(pts[num])
                    # 判断cover[term]是否重复了
                    if term in cover and term not in terms:  # 跟新terms
                        flag = False
                        for t in cover:
                            if(str(t) != str(term) and cover[t] == cover[term]):
                                flag = True
                                break
                        if flag == False:
                            return term
            if i['Expression'] == Y:
                Goal = []
                term = Y
                for pt in pts:
                    Goal.append(pt[d])
                if Goal not in SigSet:  # 不要重复值的 不需要再判断term是否重复 还是需要判断cover是否相等
                    SigSet.append(Goal)
                    i['outputData'] = Goal
                    ExpSet.append(i)
                    # Goal和ptsGoal的匹配 从0匹配到最后一个 求cover[term]
                    for num in range(ptsLength):
                        if(Goal[num] == ptsGoal[num]):
                            if term not in cover:
                                cover[term] = []
                            if pts[num] not in cover[term]:  # 不能重复把点输入cover中
                                cover[term].append(pts[num])
                        # 判断cover[term]是否重复了
                    if term in cover and term not in terms:
                        flag = False
                        for t in cover:
                            if(str(t) != str(term) and cover[t] == cover[term]):
                                flag = True
                                break
                        if(flag == False):
                            return term
    # 上面0 1 ｘ　ｙ已经枚举完了　接下来按大小枚举更大的
    # 设计下自己枚举顺序 先所有的++
    MaxSize = 2
    while(True):
        # 严格按大小枚举term
        # 单纯时term的化是不是不需要t_vocabulary集合
        # 执行add sub 如果还要添加其他的操作再加入vocabulary
        for i in t_vocabulary:
            for size1 in range(1, MaxSize):
                for choose1 in ExpSet:
                    if(choose1['size'] == size1):
                        for choose2 in ExpSet:
                            if(choose2['size'] == MaxSize-size1):
                                term = FunExg[i['Function_name']](
                                    choose1['Expression'], choose2['Expression'])
                                Goal = []  # 计算goal
                                for k, h in zip(choose1['outputData'], choose2['outputData']):
                                    Goal.append(
                                        FunExg[i['Function_name']](k, h))
                                if Goal not in SigSet:  # 更新SigSet ExgSet
                                    SigSet.append(Goal)
                                    i['outputData'] = Goal
                                    ExpSet.append(
                                        {'Expression': term, 'arity': i['arity'], 'outputData': Goal, 'size': MaxSize})
                                    if term not in terms:
                                        # term不在terms才更新cover,且要求最后一个pt必须满足term
                                        for num in range(ptsLength):
                                            if(Goal[num] == ptsGoal[num]):  # 跟新cover[term]
                                                if term not in cover:
                                                    cover[term] = []
                                                if pts[num] not in cover[term]:
                                                    cover[term].append(
                                                        pts[num])
                                        # 判断cover[term]是否重复了,先判断term是否在cover中
                                        if term in cover and term not in terms:  # 更新terms
                                            flag = False
                                            for t in cover:
                                                if(str(t) != str(term) and cover[t] == cover[term]):
                                                    flag = True
                                                    break
                                            if(flag == False):
                                                return term
        MaxSize += 1
