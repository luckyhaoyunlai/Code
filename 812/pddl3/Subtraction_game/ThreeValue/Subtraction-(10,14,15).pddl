(define (domain Subtraction_game)
	(:objects ?v1)
	(:tercondition (and (>= ?v1 0) (< ?v1 10) ))
	(:constraint (>= ?v1 0))
	(:action take
		:parameters (?k)
		:precondition (and (>= ?v1 ?k) (or (= ?k 10) (= ?k 14) (= ?k 15)))
		:effect (assign ?v1 (- ?v1 ?k)))
)