(define (domain Wythoff-Game-k-l-limited-(k=3,l=8))
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
		:precondition (and (>= ?v1 ?k) (>= ?v2 ?k) (> ?k 0) (> ?l 0) (or (and (>= (- ?v1 ?k) (- ?v2 ?l)) (>= (- ?v1 ?k) 8) (>= (- ?v2 ?l) 3)) (and (>= (- ?v2 ?l) (- ?v1 ?k)) (>= (- ?v1 ?k) 3) (>= (- ?v2 ?l) 8))))
		:effect (and (assign ?v1 (- ?v1 ?k)) (assign ?v2 (- ?v2 ?l))))
)