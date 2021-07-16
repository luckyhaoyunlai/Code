(define (domain Two-piled-pointed_NIm)
	(:objects ?v1 ?v2 ?v3)
	(:tercondition (and (= ?v1 0) (= ?v2 0)))
    (:constraint (and (>= ?v1 0) (>= ?v2 0) (> ?v3 0) (<= ?v3 2)))
    (:action take1
        :parameters (?k1 ?k2)
        :precondition (and (>= ?v1 ?k1) (= ?v3 1) (> ?k1 0) (> ?k2 0) (<= ?k2 2))
        :effect    (and (assign ?v1 (- ?v1 ?k1)) (assign ?v3 ?k2)))
    (:action take2
        :parameters (?k1 ?k2)
        :precondition (and (>= ?v2 ?k1) (= ?v3 2)  (> ?k1 0) (> ?k2 0) (<= ?k2 2))
        :effect (and (assign ?v2 (- ?v2 ?k1)) (assign ?v3 ?k2)))
)