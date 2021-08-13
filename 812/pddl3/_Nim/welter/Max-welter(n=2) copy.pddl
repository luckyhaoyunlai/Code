(define (domain welter)
	(:objects ?v1 ?v2)
	(:tercondition  (and (= ?v1 0) (= ?v2 1)) )
    (:constraint (and (>= ?v1 0) (>= ?v2 0) (> ?v2 ?v1)))
    (:action take
        :parameters (?k)
        :precondition (and (> ?k 0) (!= (- ?v2 ?k) ?v1))
        :effect (and (when (> (- ?v2 ?k) ?v1) (assign ?v2 (- ?v2 ?k))) (when (< (- ?v2 ?k) ?v1) (assign ?v2 ?v1)) (when (< (- ?v2 ?k) ?v1) (assign ?v1 (- ?v2 ?k)))))
)