import os

def generateSub1(a):
    a=str(a)
    filename = './Subtraction_game_periodic/{'+a+'}-Subtraction.pddl'
    fp = open(filename,'w') 
    fp.write('(define (domain Subtraction_game)'+'\n')
    fp.write('\t'+'(:objects ?v)'+'\n')
    fp.write('\t'+'(:type normal)'+'\n')
    fp.write('\t'+'(:tercondition (and (>= ?v 0) (< ?v '+a+') ))'+'\n')
    fp.write('\t'+'(:constraint (>= ?v 0))'+'\n')
    fp.write('\t'+'(:action take'+'\n')
    fp.write('\t'+'\t'+':parameters (?k)'+'\n')
    fp.write('\t'+'\t'+':precondition (and (>= ?v ?k) (= ?k '+a+'))'+'\n')
    fp.write('\t'+'\t'+':effect (assign ?v (- ?v ?k)))'+'\n')
    fp.write(')')
    fp.close()
    return
def generateSub2(a,b):
    a=str(a)
    b=str(b)
    filename = './Subtraction_game_periodic/{'+a+','+b+'}-Subtraction.pddl'
    fp = open(filename,'w') 
    fp.write('(define (domain Subtraction_game)'+'\n')
    fp.write('\t'+'(:objects ?v)'+'\n')
    fp.write('\t'+'(:type normal)'+'\n')
    fp.write('\t'+'(:tercondition (and (>= ?v 0) (< ?v '+a+') ))'+'\n')
    fp.write('\t'+'(:constraint (>= ?v 0))'+'\n')
    fp.write('\t'+'(:action take'+'\n')
    fp.write('\t'+'\t'+':parameters (?k)'+'\n')
    fp.write('\t'+'\t'+':precondition (and (>= ?v ?k) (= ?k '+a+') (= ?k '+b+'))'+'\n')
    fp.write('\t'+'\t'+':effect (assign ?v (- ?v ?k)))'+'\n')
    fp.write(')')
    fp.close()
    return

def generateSub3(a,b,c):
    a=str(a)
    b=str(b)
    c=str(c)
    filename = './Subtraction_game_periodic/{'+a+','+b+','+c+'}-Subtraction.pddl'
    fp = open(filename,'w') 
    fp.write('(define (domain Subtraction_game)'+'\n')
    fp.write('\t'+'(:objects ?v)'+'\n')
    fp.write('\t'+'(:type normal)'+'\n')
    fp.write('\t'+'(:tercondition (and (>= ?v 0) (< ?v '+a+') ))'+'\n')
    fp.write('\t'+'(:constraint (>= ?v 0))'+'\n')
    fp.write('\t'+'(:action take'+'\n')
    fp.write('\t'+'\t'+':parameters (?k)'+'\n')
    fp.write('\t'+'\t'+':precondition (and (>= ?v ?k) (= ?k '+a+') (= ?k '+b+') (= ?k '+c+'))'+'\n')
    fp.write('\t'+'\t'+':effect (assign ?v (- ?v ?k)))'+'\n')
    fp.write(')')
    fp.close()
    return

def generateSub4(a,b,c,d):
    a=str(a)
    b=str(b)
    c=str(c)
    d=str(d)
    filename = './Subtraction_game_periodic/{'+a+','+b+','+c+','+d+'}-Subtraction.pddl'
    fp = open(filename,'w') 
    fp.write('(define (domain Subtraction_game)'+'\n')
    fp.write('\t'+'(:objects ?v)'+'\n')
    fp.write('\t'+'(:type normal)'+'\n')
    fp.write('\t'+'(:tercondition (and (>= ?v 0) (< ?v '+a+') ))'+'\n')
    fp.write('\t'+'(:constraint (>= ?v 0))'+'\n')
    fp.write('\t'+'(:action take'+'\n')
    fp.write('\t'+'\t'+':parameters (?k)'+'\n')
    fp.write('\t'+'\t'+':precondition (and (>= ?v ?k) (= ?k '+a+') (= ?k '+b+') (= ?k '+c+') (= ?k '+d+'))'+'\n')
    fp.write('\t'+'\t'+':effect (assign ?v (- ?v ?k)))'+'\n')
    fp.write(')')
    fp.close()
    return


for a in range(1,30):
    for b in range (1,30):
        for r in range (1,30):
            if a > 1 and (b - r)%a == 0:
                generateSub3(a, b, b+2*a)
