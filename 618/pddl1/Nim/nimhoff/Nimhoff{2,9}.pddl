(define (domain nimhoff{2,9})
	(:objects ?v1 ?v2)
	(:tercondition (and (= ?v1 0) (= ?v2 0)))
	(:constraint (and (>= ?v1 0) (>= ?v2 0)))
	(:action take1
		:parameters (?k)
		:precondition (and (>= ?v1 ?k) (> ?k 0))
		:effect (assign ?v1 (- ?v1 ?k)))
	(:action take2
		:parameters (?k)
		:precondition (and (>= ?v2 ?k) (> ?k 0))
		:effect (assign ?v2 (- ?v2 ?k)))
	(:action take3
		:parameters (?k)
		:precondition (and (>= ?v2 2) (>= ?v1 9))
		:effect (and (assign ?v1 (- ?v1 2)) (assign ?v2 (- ?v2 9))))
)