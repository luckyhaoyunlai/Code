(define (domain Two-piled-pointed_NIm)
	(:objects ?v1 ?v2 ?p)
	(:tercondition (and (= ?v1 0) (= ?v2 0)))
    (:constraint (and (>= ?v1 0) (>= ?v2 0) (> ?p 0) (<= ?p 2)))
    (:action take1
        :parameters (?k ?m)
        :precondition (and (>= ?v1 ?k) (= ?p 1) (> ?k 0) (> ?m 0) (<= ?m 2))
        :effect    (and (assign ?v1 (- ?v1 ?k)) (assign ?p ?m)))
    (:action take2
        :parameters (?k ?m)
        :precondition (and (>= ?v2 ?k) (= ?p 2)  (> ?k 0) (> ?m 0) (<= ?m 2))
        :effect (and (assign ?v2 (- ?v2 ?k)) (assign ?p ?m)))
)