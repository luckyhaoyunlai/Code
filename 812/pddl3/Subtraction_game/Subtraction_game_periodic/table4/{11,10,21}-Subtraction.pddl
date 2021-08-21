(define (domain Subtraction_game)
	(:objects ?v)
	(:type normal)
	(:tercondition (and (>= ?v 0) (< ?v 11) ))
	(:constraint (>= ?v 0))
	(:action take
		:parameters (?k)
		:precondition (and (>= ?v ?k) (= ?k 11) (= ?k 10) (= ?k 21))
		:effect (assign ?v (- ?v ?k)))
)