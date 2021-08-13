(define (domain NimG)
	(:objects ?v1 ?v2 ?v3 ?v4)
	(:tercondition    (and  (or (and (= ?v1 0) (= ?v4 1)) (and (= ?v2 0) (= ?v4 2)) (and (= ?v3 0) (= ?v4 3))) (>= ?v1 0) (>= ?v2 0) (>= ?v3 0)(> ?v4 0) (<= ?v4 3)))
    (:constraint (and (>= ?v1 0) (>= ?v2 0) (>= ?v3 0)(> ?v4 0) (<= ?v4 3)))
    (:action take1
        :parameters (?k)
        :precondition (and (>= ?v1 ?k) (> ?k 0) (= ?v4 1))
        :effect (and (assign ?v1 (- ?v1 ?k)) (assign ?v4 2)))
    (:action take2
        :parameters (?k1 ?k2)
        :precondition (and (>= ?v2 ?k1) (> ?k1 0) (= ?v4 2) (or (= ?k2 1) (= ?k2 3)))
        :effect (and (assign ?v2 (- ?v2 ?k)) (assign ?v4 ?k2)))
    (:action take3
        :parameters (?k)
        :precondition (and (>= ?v3 ?k) (> ?k 0) (= ?v4 3))70,      
        :effect (and (assign ?v3 (- ?v3 ?k)) (assign ?v4 2)))
)