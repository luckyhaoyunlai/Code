#2-chomp-game
# actions = [{"action_name": "eat1", "precondition": And(X >= k_num, k_num > 1), "transition_formula": And(And(X >= k_num, k_num > 1), Y == k_num - 1, Implies(X1 >= k_num, Y1 == k_num - 1), Or(X1 >= k_num, Y1 == X1))},
#            {"action_name": "eat2", "precondition": And(X1 >= k_num, k_num > 0), "transition_formula": And(And(X1 >= k_num, k_num > 0), Y1 == k_num - 1, Y == X)}]
# Game = {"Terminal_Condition": And(X == 1, X1 == 0),
#         "actions": actions,
#         "Constraint": And(X >= 1, X1 >= 0, X >= X1),
#         "var_num": 2,
#         "appeal_constants": []}


#empty and divide
# actions = [{"action_name": "empty1", "precondition": And(X1 > k_num, k_num >= 1), "transition_formula": And(And(X1 > k_num, k_num >= 1), And(Y == k_num, Y1 == X1 - k_num))},
#            {"action_name": "empty2", "precondition": And(X > k_num, k_num >= 1), "transition_formula": And(And(X > k_num, k_num >= 1), And(Y1 == k_num, Y == X - k_num))}]
# Game = {"Terminal_Condition": And(X == 1, X1 == 1),
#         "actions": actions,
#         "Constraint": And(X >= 1, X1 >= 1),
#         "var_num": 2,
#         "appeal_constants": []}

# L_shaped_chomp_game
# actions=[{"action_name": "eat1", "precondition":And(X >= k_num, k_num > 1),
#     "transition_formula": And(And(X >= k_num, k_num > 1), Y == k_num - 1, Y1 == X1)},
#     {"action_name": "eat2", "precondition":And(X1 >= k_num, k_num > 1),
#     "transition_formula": And(And(X1 >= k_num, k_num > 1), Y1 == k_num - 1, Y == X)}]
# Game = {"Terminal_Condition": And(X == 1, X1 == 1),
#         "actions": actions,
#         "Constraint":  And(X >= 1, X1 >= 1),
#         "var_num": 2,
#         "appeal_constants": []} 

# Max_min_two_piled_nim
# actions = [{"action_name": "take1", "precondition":And(X >= k_num, k_num >= 1) , "transition_formula":
#     And(And(X >= k_num, k_num >= 1),
#     And(And(And(X - k_num >= X1, Y == X - k_num),
#             X - k_num < X1,
#             Y1 == X - k_num),
#             X - k_num < X1,
#             Y == X1),
#     Or(Or(X - k_num < X1, Y==X),
#        Or(Or(X - k_num < X1, Y1==X1),
#           Or(X - k_num >= X1, Y == X))))},
#            {"action_name": "take2", "precondition": And(X1 >= k_num, k_num >= 1) , "transition_formula": And(And(X1 >= k_num, k_num >= 1), Y1 == X1 - k_num, Y == X)}]
# Game = {"Terminal_Condition":And(X == 0, X1 == 0) ,
#         "actions": actions,
#         "Constraint":And(X >= 0, X1 >= 0) ,
#         "var_num": 2,
#         "appeal_constants": []}

# Monotonic_2_piled_nim
# actions = [{"action_name": "take1", "precondition":And(X >= k_num, k_num >= 1) , "transition_formula": And(And(X >= k_num, k_num >= 1), Y == X - k_num, Y1 == X1)},
#            {"action_name": "take2", "precondition":And(X1 - k_num >= X, k_num >= 1), "transition_formula":And(And(X1 - k_num >= X, k_num >= 1), Y1 == X1 - k_num, Y == X)}]
# Game = {"Terminal_Condition":And(X == 0, X1 == 0) ,
#         "actions": actions,
#         "Constraint":And(X >= 0, X1 >= 0),
#         "var_num": 2,
#         "appeal_constants": []}

# monotonic_2_diet_wythoff_game
# actions=[{"action_name":"take1","precondition":Or(And(k_num == 1, X > 0), And(k_num == 2, X > 1)),"transition_formula": And( Or(And(k_num == 1, X > 0), And(k_num == 2, X > 1)),Y == X - k_num, Y1 == X1)},
#          {"action_name": "take2", "precondition":Or(And(k_num == 1, X1 > X), And(k_num == 2, X1 > X + 1)),"transition_formula": And(Or(And(k_num == 1, X1 > X), And(k_num == 2, X1 > X + 1)),Y1==X1-k_num,Y==X)},
#          {"action_name": "takeBoth", "precondition":And(X ==X1 , X > 0),"transition_formula": And(And(X ==X1 , X > 0),Y==X-1,Y1==X1-1)}]
# Game= {"Terminal_Condition":And(X == 0, X1 == 0),
#        "actions":actions,
#        "Constraint":And(X >= 0, X1 >= X),
#        "var_num":2,
#        "appeal_constants":[]}

# two_piled_nim
# actions = [{"action_name": "take1", "precondition": And(X >= k_num, k_num >= 1) , "transition_formula":And(And(X >= k_num, k_num >= 1), Y == X - k_num, Y1 == X1)},
#            {"action_name": "take2", "precondition": And(X1 >= k_num, k_num >= 1) , "transition_formula":And(And(X1 >= k_num, k_num >= 1), Y1 == X1 - k_num, Y == X)}]
# Game = {"Terminal_Condition": And(X == 0, X1 == 0) ,
#         "actions": actions,
#         "Constraint": And(X >= 0, X1 >= 0),
#         "var_num": 2,
#         "appeal_constants": []} 


# Wythoff_game_odd_even max还未定义
# actions = [{"action_name": "take1", "precondition": And(X >= k_num, k_num > 0, k_num <= max, (X - k_num)%2 == 1) , "transition_formula":And(And(X >= k_num, k_num > 0, k_num <= max, (X - k_num)%2 == 1), Y == X - k_num,Y1 == X1)},
#            {"action_name": "take2", "precondition":And(X1 >= k_num, k_num > 0, k_num <= max) , "transition_formula":
#            And(And(X1 >= k_num, k_num > 0, k_num <= max), Y1 == X1 - k_num, Y == X)},
#            {"action_name": "take3", "precondition":And(X >= k_num, X1 >= k_num, k_num > 0, k_num <= max) , "transition_formula":
#            And(And(X >= k_num, X1 >= k_num, k_num > 0, k_num <= max),And(Y == X - k_num, Y1 == X1 - k_num))}]
# Game = {"Terminal_Condition": And(X == 0, X1 == 0) ,
#         "actions": actions,
#         "Constraint":Or(X > 0, X1 > 0),
#         "var_num": 2,
#         "appeal_constants": []} 

# Subtraction_game s={1,2,4}
# actions = [{"action_name": "take", "precondition":And(X >= k_num, Or(k_num == 1, k_num == 2, k_num == 5)) , 
#             "transition_formula":And(And(X >= k_num,Or(k_num == 1, k_num == 2, k_num == 5)), Y == X - k_num)}]
# Game = {"Terminal_Condition": And(X >= 0, X < 1),
#         "actions": actions,
#         "Constraint":X >= 0,
#         "var_num": 1,
#         "appeal_constants": []} 