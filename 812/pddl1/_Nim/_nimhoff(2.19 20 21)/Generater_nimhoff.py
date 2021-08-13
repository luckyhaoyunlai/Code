import os

def generateNimhoff(i,j):
    i=str(i)
    j=str(j)
    filename = 'pddl1\_Nim\_nimhoff\_nimhoff{'+i+','+j+'}.pddl'
    fp = open(filename,'w') 
    fp.write('(define (domain nimhoff_'+i+'_'+j+'_)'+'\n')
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
    fp.write('\t'+'\t'+':precondition (and (>= ?v2 '+i+') (>= ?v1 '+j+'))'+'\n')
    fp.write('\t'+'\t'+':effect (and (assign ?v1 (- ?v1 '+i+')) (assign ?v2 (- ?v2 '+j+'))))'+'\n')
    fp.write(')')
    fp.close()
    return


for i in range(1,10):
    for j in range(1,10):
        generateNimhoff(i,j)
