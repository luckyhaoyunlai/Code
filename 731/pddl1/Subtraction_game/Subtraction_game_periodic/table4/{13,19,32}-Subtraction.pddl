(define (domain Subtraction_game)
	(:objects ?v)
	(:type normal)
	(:tercondition (and (>= ?v 0) (< ?v 13) ))
	(:constraint (>= ?v 0))
	(:action take
		:parameters (?k)
		:precondition (and (>= ?v ?k) (= ?k 13) (= ?k 19) (= ?k 32))
		:effect (assign ?v (- ?v ?k)))
)