(define (domain odd-or-even-nim)
	(:objects ?v ?s)
	(:tercondition (= ?v 0))
	(:constraint (and (>= ?v 0) (>= ?s 0) (<= ?s 1)))
	(:action odd-take-then-even
		:parameters (?k)
		:precondition (and (>= ?k 1) (%= ?k 2 1) (= ?s 0) (>= ?v ?k))
		:effect (and (assign ?v (- ?v ?k)) (assign ?s 1)))
	(:action odd-take-then-odd
		:parameters (?k)
		:precondition (and (>= ?k 1) (%= ?k 2 1) (= ?s 0) (>= ?v ?k))
		:effect (and (assign ?v (- ?v ?k)) (assign ?s 0)))
	(:action even-take-then-even
		:parameters (?k)
		:precondition (and (>= ?k 1) (%= ?k 2 0) (= ?s 1) (>= ?v ?k))
		:effect (and (assign ?v (- ?v ?k)) (assign ?s 1)))
	(:action even-take-then-odd
		:parameters (?k)
		:precondition (and (>= ?k 1) (%= ?k 2 0) (= ?s 1) (>= ?v ?k))
		:effect (and (assign ?v (- ?v ?k)) (assign ?s 0)))
)