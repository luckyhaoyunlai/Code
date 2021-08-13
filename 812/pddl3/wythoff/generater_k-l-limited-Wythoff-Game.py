import os

def generateKLwythoff(i,j):
    i=str(i)
    j=str(j)
    filename = './wythoff/Wythoff-Game-k-l-limited(k='+i+',l='+j+').pddl'
    fp = open(filename,'w') 
    fp.write('(define (domain Wythoff-Game-k-l-limited-(k='+i+',l='+j+'))'+'\n')
    fp.write('\t'+'(:objects ?v1 ?v2)'+'\n')
    fp.write('\t'+'(:tercondition (and (= ?v1 0) (= ?v2 0)))'+'\n')
    fp.write('\t'+'(:constraint (and (>= ?v1 0) (>= ?v2 0)))'+'\n')
    fp.write('\t'+'(:action take1'+'\n')
    fp.write('\t'+'\t'+':parameters (?k)'+'\n')
    fp.write('\t'+'\t'+':precondition (and (>= ?v1 ?k) (> ?k 0))'+'\n')
    fp.write('\t'+'\t'+':effect (assign ?v1 (- ?v1 ?k)))'+'\n')
    fp.write('\t'+'(:action take2'+'\n')
    fp.write('\t'+'\t'+':parameters (?k)'+'\n')
    fp.write('\t'+'\t'+':precondition (and (>= ?v2 ?k) (> ?k 0))'+'\n')
    fp.write('\t'+'\t'+':effect (assign ?v2 (- ?v2 ?k)))'+'\n')
    fp.write('\t'+'(:action take3'+'\n')
    fp.write('\t'+'\t'+':parameters (?k)'+'\n')
    fp.write('\t'+'\t'+':precondition (and (>= ?v1 ?k) (>= ?v2 ?k) (> ?k 0) (> ?l 0) (or (and (>= (- ?v1 ?k) (- ?v2 ?l)) (>= (- ?v1 ?k) '+j+') (>= (- ?v2 ?l) '+i+')) (and (>= (- ?v2 ?l) (- ?v1 ?k)) (>= (- ?v1 ?k) '+i+') (>= (- ?v2 ?l) '+j+'))))'+'\n')
    fp.write('\t'+'\t'+':effect (and (assign ?v1 (- ?v1 ?k)) (assign ?v2 (- ?v2 ?l))))'+'\n')
    fp.write(')')
    fp.close()
    return


for i in range(1,10):
    for j in range(1,10):
        if i < j:
            generateKLwythoff(i,j)
