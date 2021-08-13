import os


path = os.getcwd()
path = path + '\\pddl1\_Nim\Anther_nim\I-mark'

def generate(t,d):
    t1=t-1
    t1=str(t1)
    t=str(t)
    d1=str(d)
    
    filename = path+'\T,d-I-Mark-Game{'+t+','+d1+'}.pddl'
    fp = open(filename,'w') 
    fp.write('(define (domain  i-mark-Game)'+'\n')
    fp.write('\t'+'(:objects ?v1)'+'\n')
    fp.write('\t'+'(:tercondition (= ?v1 0))'+'\n')
    fp.write('\t'+'(:constraint (>= ?v1 0))'+'\n')
    fp.write('\t'+'(:action take1'+'\n')
    fp.write('\t'+'\t'+':parameters (?k)'+'\n')
    fp.write('\t'+'\t'+':precondition (and (<= ?k '+t1+') (> ?k 0) (>= ?v1 ?k))'+'\n')
    fp.write('\t'+'\t'+':effect (assign ?v1 (- ?v1 ?k)))'+'\n')
    fp.write('\t'+'(:action take2'+'\n')
    fp.write('\t'+'\t'+':parameters (?k)'+'\n')
    if d==2:
        fp.write('\t'+'\t'+':precondition (and (= ?v1 (+ ?k ?k)) (> ?v1 ?k))'+'\n')
    elif d==3:
        fp.write('\t'+'\t'+':precondition (and (= ?v1 (+ ?k (+ ?k ?k))) (> ?v1 ?k))'+'\n')
    elif d==4:
        fp.write('\t'+'\t'+':precondition (and (= ?v1 (+ ?k (+ ?k (+ ?k ?k)))) (> ?v1 ?k))'+'\n')
    elif d==5:
        fp.write('\t'+'\t'+':precondition (and (= ?v1 (+ ?k (+ ?k (+ ?k (+ ?k ?k))))) (> ?v1 ?k))'+'\n')
    elif d==6:
        fp.write('\t'+'\t'+':precondition (and (= ?v1 (+ ?k (+ ?k (+ ?k (+ ?k (+ ?k ?k)))))) (> ?v1 ?k))'+'\n')
    elif d==7:
        fp.write('\t'+'\t'+':precondition (and (= ?v1 (+ ?k (+ ?k (+ ?k (+ ?k (+ ?k (+ ?k ?k))))))) (> ?v1 ?k))'+'\n')
    elif d==8:
        fp.write('\t'+'\t'+':precondition (and (= ?v1 (+ ?k (+ ?k (+ ?k (+ ?k (+ ?k (+ ?k (+ ?k ?k)))))))) (> ?v1 ?k))'+'\n')
    elif d==9:
        fp.write('\t'+'\t'+':precondition (and (= ?v1 (+ ?k (+ ?k (+ ?k (+ ?k (+ ?k (+ ?k (+ ?k (+ ?k ?k))))))))) (> ?v1 ?k))'+'\n')
    elif d==10:
        fp.write('\t'+'\t'+':precondition (and (= ?v1 (+ ?k (+ ?k (+ ?k (+ ?k (+ ?k (+ ?k (+ ?k (+ ?k (+ ?k ?k)))))))))) (> ?v1 ?k))'+'\n')
    fp.write('\t'+'\t'+':effect (assign ?v1  ?k))'+'\n')
    fp.write(')')
    fp.close()
    return
for t in range(2,10):
    for d in range(2,10):
        if d % t != 1:
            generate(t,d)
