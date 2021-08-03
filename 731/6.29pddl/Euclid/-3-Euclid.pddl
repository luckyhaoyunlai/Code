(define (domain Euclid)
	(:objects ?v1 ?v2 ?v3)
	(:tercondition  (and (= ?v1 ?v2) (= ?v1 ?v3) (= ?v2 ?v3)))
    (:constraint (and (>= ?v1 0) (>= ?v2 0)))
    (:action take1
        :parameters (?k)
        :precondition (and (>= ?v1 ?k) (> ?k 0) (or (%= ?k ?v2 0) (%= ?k ?v3 0) )  )
        :effect (and (when (>= (- ?v1 ?k) ?v2) (assign ?v1 (- ?v1 ?k)))  (when (< (- ?v1 ?k) ?v3) (assign ?v3 (- ?v1 ?k))) (when (< (- ?v1 ?k) ?v3) (assign ?v2 ?v3)) (when (< (- ?v1 ?k) ?v3) (assign ?v1 ?v2))))
    (:action take2
        :parameters (?k)
        :precondition (and (>= ?v2 ?k) (> ?k 0) (%= ?k ?v3 0))
        :effect (and (when (>= (- ?v2 ?k) ?v3) (assign ?v2 (- ?v2 ?k))) (when (<= (- ?v2 ?k) ?v3) (assign ?v3 (- ?v2 ?k))) (when (<= (- ?v2 ?k) ?v3) (assign ?v2  ?v3))))
)