(define (domain Two-piled-nim)
	(:objects ?v1 ?v2)
	(:tercondition (or (= ?v1 0) (= ?v2 0) ))
    (:constraint (and (>= ?v1 0) (>= ?v2 0)))
    (:action take1
        :parameters (?k)
        :precondition (and (>= ?v1 ?k) (> ?k 0) (%= ?k ?v2 0))
        :effect (assign ?v1 (- ?v1 ?k)))
    (:action take2
        :parameters (?k)
        :precondition (and (>= ?v2 ?k) (> ?k 0) (%= ?k ?v1 0))
        :effect (assign ?v2 (- ?v2 ?k)))
)