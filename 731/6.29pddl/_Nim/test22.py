def printLN(i,j,k,o):
    print("\hline \n %d & %d & %d & %d  \\\\" %(i,j,k,o))

# for i in range(0,30):
#     if i % 4  == 0:
#         j = i+3
#         k = i^j
#         o = 3
#         printLN(i,j,k,o)
#     if i % 4  == 1:
#         j = i+1
#         k = i^j
#         o = 1
#         printLN(i,j,k,o)


for i in range(0,50):
    for j in range(0,50):
        if i<j and i^j == 8 :
            print(i,j,j-i)