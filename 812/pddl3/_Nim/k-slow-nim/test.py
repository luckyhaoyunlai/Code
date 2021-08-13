import os

path = os.getcwd() + '\\pddl'
path = path.replace('\\','/')


def generate(i):
    i= str(i)
    filename = path + '/Two-piled-'+i+'-slow-nim.pddl'
    fp = open(filename,'w') 
    a='''(define (domain Two-piled-k-slow-nim)
	(:objects ?v1 ?v2)
	(:tercondition (and (= ?v1 0) (= ?v2 0)))
    (:constraint (and (>= ?v1 0) (>= ?v2 0)))
    (:action take1
        :parameters (?k)
        :precondition (and (>= ?v1 ?k) (> ?k 0) (<= ?k %s))
        :effect (assign ?v1 (- ?v1 ?k)))
    (:action take2
        :parameters (?k)
        :precondition (and (>= ?v2 ?k) (> ?k 0) (<= ?k %s))
        :effect (assign ?v2 (- ?v2 ?k)))
)'''%(i,i)
    fp.write(a)


    fp.close()
    return

for i in range(1,31):
    generate(i)

