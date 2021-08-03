import os

path = os.getcwd()
path = path + '\\pddl1\\_Nim\\Anther_nim\\I-mark'
print(path)
print (os.listdir(path))
for item in os.listdir(path):
    print(item)