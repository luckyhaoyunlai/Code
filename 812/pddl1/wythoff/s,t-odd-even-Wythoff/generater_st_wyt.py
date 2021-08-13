import os

def generateSTWyt(s,t):
    s1=str(s)
    t1=str(t)
    s =s - 1
    s = str(s)
    t = str(t)
    filename = './s,t-odd-even-Wythoff/S,T-odd-even-('+s1+','+t1+')-wythoff.pddl'
    fp = open(filename,'w') 
    fp.write('(define (domain Wythoff_game)'+'\n')
    fp.write('\t'+'(:objects ?v1 ?v2)'+'\n')
    fp.write('\t'+'(:tercondition (and (= ?v1 0) (= ?v2 0)))'+'\n')
    fp.write('\t'+'(:constraint (and (>= ?v1 0) (>= ?v2 0)))'+'\n')
    fp.write('\t'+'(:action take1'+'\n')
    fp.write('\t'+'\t'+':parameters (?k)'+'\n')
    fp.write('\t'+'\t'+':precondition (and (>= ?v1 ?k) (> ?k 0) (%= ?k 2 1))'+'\n')
    fp.write('\t'+'\t'+':effect (assign ?v1 (- ?v1 ?k)))'+'\n')
    fp.write('\t'+'(:action take2'+'\n')
    fp.write('\t'+'\t'+':parameters (?k)'+'\n')
    fp.write('\t'+'\t'+':precondition (and (>= ?v2 ?k) (> ?k 0) (%= ?k 2 0))'+'\n')
    fp.write('\t'+'\t'+':effect (assign ?v2 (- ?v2 ?k)))'+'\n')
    fp.write('\t'+'(:action take3'+'\n')
    fp.write('\t'+'\t'+':parameters (?k ?l)'+'\n')
    fp.write('\t'+'\t'+':precondition (and (>= ?v1 ?k) (> ?k 0) (%= ?k 2 1)  (>= ?v2 ?l) (> ?l 0) (%= ?l 2 0)  (or(and(> ?k ?l) (> (+ '+t+' (* ?l '+s+')) (- ?k ?l) ) ) (and(> ?l ?k) (> (+ '+t+' (* ?k '+s+')) (- ?l ?k) )  ) ))'+'\n')
    fp.write('\t'+'\t'+':effect (and (assign ?v1 (- ?v1 ?k)) (assign ?v2 (- ?v2 ?l))))'+'\n')
    fp.write(')')


    fp.close()
    return

for i in range (1,4):
    for j in range (1,11):
        generateSTWyt(i, j)
