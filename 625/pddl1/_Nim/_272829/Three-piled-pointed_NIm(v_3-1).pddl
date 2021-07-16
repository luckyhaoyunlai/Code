(define (domain Three-piled-pointed_NIm)
	(:objects ?v1 ?v2 ?v3 ?v4)
	(:tercondition (and (= ?v1 0) (= ?v2 0) (= ?v3 0)))
    (:constraint (and (>= ?v1 0) (>= ?v2 0) (>= ?v3 0) (<= ?v3 1) (> ?v4 0) (<= ?v4 3)))
    (:action take1
        :parameters (?k ?k1)
        :precondition (and (>= ?v1 ?k) (= ?v4 1) (> ?k 0) (> ?k1 0) (<= ?k1 3))
        :effect    (and (assign ?v1 (- ?v1 ?k)) (assign ?v4 ?k1)))
    (:action take2
        :parameters (?k ?k1)
        :precondition (and (>= ?v2 ?k) (= ?v4 2)  (> ?k 0) (> ?k1 0) (<= ?k1 3))
        :effect (and (assign ?v2 (- ?v2 ?k)) (assign ?v4 ?k1)))
    (:action take3
        :parameters (?k ?k1)
        :precondition (and (>= ?v3 ?k) (= ?v4 3)  (> ?k 0) (> ?k1 0) (<= ?k1 3))
        :effect (and (assign ?v2 (- ?v2 ?k)) (assign ?v4 ?k1)))
)