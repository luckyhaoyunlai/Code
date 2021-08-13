(define (domain Subtraction_game)
	(:objects ?v)
	(:type normal)
	(:tercondition (and (>= ?v 0) (< ?v 14) ))
	(:constraint (>= ?v 0))
	(:action take
		:parameters (?k)
		:precondition (and (>= ?v ?k) (= ?k 14) (= ?k 6) (= ?k 20))
		:effect (assign ?v (- ?v ?k)))
)