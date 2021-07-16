(define (domain nimhoff{3,2})
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
		:precondition (and (>= ?v2 3) (>= ?v1 2))
		:effect (and (assign ?v1 (- ?v1 3)) (assign ?v2 (- ?v2 2))))
)