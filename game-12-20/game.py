# 
L-shaped Chomp game
actions=[{"action_name":"eat1","precondition":And(X >= k_num, k_num > 1),"transition_formula": And(And(X >= k_num, k_num > 1), Y == k_num - 1, Y1 == X1)},
         {"action_name": "eat2", "precondition": And(X1 >= k_num, k_num > 1),"transition_formula": And(And(X1 >= k_num, k_num > 1), Y1 == k_num - 1, Y == X)}]
Game= {"Terminal_Condition":And(X == 1, X1 == 1),
       "actions":actions,
       "Constraint":And(X >= 1, X1 >= 1),
       "var_num":2,
       "appeal_constants":[]}

# Chomp game(2 x n)
# actions=[{"action_name":"eat1","precondition":And(X >= k_num, k_num > 1),"transition_formula": And(And(X >= k_num, k_num > 1), Y == k_num - 1,Implies(X1 >= k_num, Y1 == k_num - 1),Or(X1 >= k_num, Y1 == X1))},
#          {"action_name": "eat2", "precondition": And(X1 >= k_num, k_num > 0),"transition_formula": And(And(X1 >= k_num, k_num > 0), Y1 == k_num - 1, Y == X)}]
# Game= {"Terminal_Condition":And(X == 1, X1 == 0),
#        "actions":actions,
#        "Constraint":And(X >= 1, X1 >= 0, X >= X1),
#        "var_num":2, 
#        "appeal_constants":[]}

# Empty-and-divide
# actions=[{"action_name":"empty1","precondition":And(X1 > k_num, k_num >= 1),"transition_formula": And(And(X1 > k_num, k_num >= 1),And(Y == k_num, Y1 == X1 - k_num))},
#          {"action_name": "empty2", "precondition": And(X > k_num, k_num >= 1),"transition_formula": And(And(X > k_num, k_num >= 1),And(Y1 == k_num, Y == X - k_num))}]
# Game= {"Terminal_Condition":And(X == 1, X1 == 1),
#        "actions":actions,
#        "Constraint":And(X >= 1, X1 >= 1),
#        "var_num":2, "appeal_constants":[]}


# take-away-game
# actions=[{"action_name":"take","precondition":And(k_num >= 1, k_num <= 4, X >= k_num),"transition_formula": And(Y==X-k_num,And(X>=k_num,k_num<=4,k_num>0))}]
# Game= {"Terminal_Condition":X == 0,
#        "actions":actions,
#        "Constraint":X>=0,
#        "var_num":1,
#        "appeal_constants":[]}


# Subtraction-game
# Sub_set=(1,3,5)
# actions=[{"action_name":"take","precondition":And(Or(k_num==Sub_set[0],k_num==Sub_set[1],k_num==Sub_set[2]),X>=k_num),"transition_formula": And(Or(k_num==Sub_set[0],k_num==Sub_set[1],k_num==Sub_set[2]),X>=k_num,Y==X-k_num)}]
# Game= {"Terminal_Condition":And(X >= 0,X<min(Sub_set)),
#        "actions":actions,
#        "Constraint":And(X>=0,Y>=0),
#        "var_num":1,
#        "appeal_constants":[]}


# Monotonic 2-piled Nim
# actions=[{"action_name":"take1","precondition":And(X >= k_num, k_num >= 1),"transition_formula": And(And(X >= k_num, k_num >= 1), Y == X - k_num, Y1 == X1)},
#          {"action_name": "take2", "precondition": And(X1-k_num>=X, k_num >= 1),"transition_formula": And(And(X1 - k_num >= X, k_num >= 1),Y1 == X1 - k_num,Y == X)}]
# Game= {"Terminal_Condition":And(X == 0, X1 == 0),
#        "actions":actions,
#        "Constraint":And(X >= 0, X1 >= X),
#        "var_num":2}


# 2-piled Nim
# actions=[{"action_name":"take1","precondition":And(X >= k_num, k_num >= 1),"transition_formula": And(And(X >= k_num, k_num >= 1), Y == X - k_num, Y1 == X1)},
#          {"action_name": "take2", "precondition": And(X1 >= k_num, k_num >= 1),"transition_formula": And(And(X1 >= k_num, k_num >= 1),Y1 == X1 - k_num,Y == X)}]
# Game= {"Terminal_Condition":And(X == 0, X1 == 0),
#        "actions":actions,
#        "Constraint":And(X >= 0, X1 >= 0),
#        "var_num":2,
#        "appeal_constants":[]}

#Monotonic 2-piled Nim
# actions=[{"action_name":"eat1","precondition":And(X >= k_num, k_num > 1),"transition_formula": And(And(X >= k_num, k_num > 1), Y == k_num - 1,Implies(X1 >= k_num, Y1 == k_num - 1),Or(X1 >= k_num, Y1 == X1))},
#          {"action_name": "eat2", "precondition": And(X1 >= k_num, k_num > 0),"transition_formula": And(And(X1 >= k_num, k_num > 0), Y1 == k_num - 1, Y == X)}]
# Game= {"Terminal_Condition":And(X == 1, X1 == 0),
#        "actions":actions,
#        "Constraint":And(X >= 1, X1 >= 0, X >= X1),
#        "var_num":2,
#        "appeal_constants":[]}


from z3.z3 import And


# Monotonic 2-piled Nim wythoff
actions=[{"action_name":"take1","precondition":Or(And(k_num == 1, X > 0), And(k_num == 2, X > 1)),"transition_formula": And( Or(And(k_num == 1, X > 0), And(k_num == 2, X > 1)),Y == X - k_num, Y1 == X1)}
         {"action_name": "take2", "precondition":Or(And(k_num == 1, X1 > X), And(k_num == 2, X1 > X + 1)),"transition_formula": And(Or(And(k_num == 1, X1 > X), And(k_num == 2, X1 > X + 1)),Y1==X1-k_num,Y==X)}
         {"action_name": "takeBoth", "precondition":And(X ==X1 , X > 0),"transition_formula": And(And(X ==X1 , X > 0),Y==X-1,Y1==X1-1)}]
Game= {"Terminal_Condition":And(X == 0, X1 == 0),
       "actions":actions,
       "Constraint":And(X >= 0, X1 >= X),
       "var_num":2,
       "appeal_constants":[]}


