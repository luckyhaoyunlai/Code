(define (domain Empty-and-Redistribute)
	(:objects ?v1 ?v2 ?v3 ?v4)
	(:tercondition (> 5 (+ ?v1 (+ ?v2 (+ ?v3 ?v4)))))
    (:constraint (and (>= ?v1 1) (>= ?v2 1) (>= ?v3 1) (>= ?v4 1)))
    (:action empty1
        :parameters (?k1 ?k2 ?k3 ?k4)
        :precondition (and (> (+ ?v2 (+ ?v3 ?v4)) 3) (= (+ ?v2 (+ ?v3 ?v4)) (+ ?k1 (+ ?k2 (+ ?k3 ?k4)))) (> ?k1 0) (> ?k2 0) (> ?k3 0) (> ?k4 0) )
        :effect (and (assign ?v1 ?k1) (assign ?v2 ?k2) (assign ?v3 ?k3) (assign ?v4 ?k4)))
    (:action empty2
        :parameters (?k1 ?k2 ?k3 ?k4)
        :precondition (and (> (+ ?v1 (+ ?v3 ?v4)) 3) (= (+ ?v1 (+ ?v3 ?v4)) (+ ?k1 (+ ?k2 (+ ?k3 ?k4)))) (> ?k1 0) (> ?k2 0) (> ?k3 0) (> ?k4 0) )
        :effect (and (assign ?v1 ?k1) (assign ?v2 ?k2) (assign ?v3 ?k3) (assign ?v4 ?k4)))
    (:action empty3
        :parameters (?k1 ?k2 ?k3 ?k4)
        :precondition (and (> (+ ?v1 (+ ?v2 ?v4)) 3) (= (+ ?v1 (+ ?v2 ?v4)) (+ ?k1 (+ ?k2 (+ ?k3 ?k4)))) (> ?k1 0) (> ?k2 0) (> ?k3 0) (> ?k4 0) )
        :effect (and (assign ?v1 ?k1) (assign ?v2 ?k2) (assign ?v3 ?k3) (assign ?v4 ?k4)))
    (:action empty4
        :parameters (?k1 ?k2 ?k3 ?k4)
        :precondition (and (> (+ ?v1 (+ ?v2 ?v3)) 3) (= (+ ?v1 (+ ?v2 ?v3)) (+ ?k1 (+ ?k2 (+ ?k3 ?k4)))) (> ?k1 0) (> ?k2 0) (> ?k3 0) (> ?k4 0) )
        :effect (and (assign ?v1 ?k1) (assign ?v2 ?k2) (assign ?v3 ?k3) (assign ?v4 ?k4)))
)