(define (domain Subtraction_game)
	(:objects ?v1)
	(:tercondition (and (>= ?v1 0) (< ?v1 6) ))
	(:constraint (>= ?v1 0))
	(:action take
		:parameters (?k)
		:precondition (and (>= ?v1 ?k) (or (= ?k 6) (= ?k 10) (= ?k 13)))
		:effect (assign ?v1 (- ?v1 ?k)))
)