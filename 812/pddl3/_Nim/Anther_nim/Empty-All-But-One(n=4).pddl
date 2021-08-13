(define (domain Empty-All-But-One)
	(:objects ?v1 ?v2 ?v3 ?v4)
	(:tercondition (and (< ?v1 4) (< ?v2 4) (< ?v3 4) (< ?v4 4)))
    (:constraint (and (>= ?v1 1) (>= ?v2 1) (>= ?v3 1) (>= ?v4 1)))
    (:action keep1
        :parameters (?k1 ?k2 ?k3 ?k4)
        :precondition (and (> ?v1 4) (> ?k1 0) (> ?k2 0) (> ?k3 0) (> ?k4 0))
        :effect (and (assign ?v1 ?k1) (assign ?v2 ?k2) (assign ?v3 ?k3) (assign ?v4 ?k4)))
    (:action keep2
        :parameters (?k1 ?k2 ?k3 ?k4)
        :precondition (and (> ?v2 4) (> ?k1 0) (> ?k2 0) (> ?k3 0) (> ?k4 0))
        :effect (and (assign ?v1 ?k1) (assign ?v2 ?k2) (assign ?v3 ?k3) (assign ?v4 ?k4)))
    (:action keep3
        :parameters (?k1 ?k2 ?k3 ?k4)
        :precondition (and (> ?v3 4) (> ?k1 0) (> ?k2 0) (> ?k3 0) (> ?k4 0))
        :effect (and (assign ?v1 ?k1) (assign ?v2 ?k2) (assign ?v3 ?k3) (assign ?v4 ?k4)))
    (:action keep3
        :parameters (?k1 ?k2 ?k3 ?k4)
        :precondition (and (> ?v4 4) (> ?k1 0) (> ?k2 0) (> ?k3 0) (> ?k4 0))
        :effect (and (assign ?v1 ?k1) (assign ?v2 ?k2) (assign ?v3 ?k3) (assign ?v4 ?k4)))
)