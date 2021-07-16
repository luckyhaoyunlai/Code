(define (domain Subtraction_game)
	(:objects ?v)
	(:type normal)
	(:tercondition (and (>= ?v 0) (< ?v 18) ))
	(:constraint (>= ?v 0))
	(:action take
		:parameters (?k)
		:precondition (and (>= ?v ?k) (= ?k 18) (= ?k 22) (= ?k 40))
		:effect (assign ?v (- ?v ?k)))
)