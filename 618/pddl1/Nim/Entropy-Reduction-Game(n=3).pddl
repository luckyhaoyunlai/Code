(define (domain Entropy-Reduction-Game)
	(:objects ?v1 ?v2 ?v3)
	(:tercondition (and (<= (- ?v2 ?v1) 1) (<= (- ?v1 ?v2) 1) (<= (- ?v3 ?v2) 1) (<= (- ?v2 ?v3) 1) (<= (- ?v1 ?v3) 1) (<= (- ?v3 ?v1) 1)))
    (:constraint (and (>= ?v1 1) (>= ?v2 1) (>= ?v3 1)))
    (:action take1
        :parameters (?k ?i)
        :precondition (or (and (= ?i 2) (> ?v1 ?v2) (> ?k 0) (> (- ?v1 ?v2) ?k)) (and (= ?i 3) (> ?v1 ?v3) (> ?k 0) (> (- ?v1 ?v3) ?k)))
        :effect (and (assign ?v1 (- ?v1 ?k)) (when (= ?i 2) (assign ?v2 (+ ?v2 ?k))) (when (= ?i 2) (assign ?v2 (+ ?v2 ?k)))))
    (:action take2
        :parameters (?k ?i)
        :precondition (or (and (= ?i 1) (> ?v2 ?v1) (> ?k 0) (> (- ?v2 ?v1) ?k)) (and (= ?i 3) (> ?v2 ?v3) (> ?k 0) (> (- ?v2 ?v3) ?k)))
        :effect (and (assign ?v2 (- ?v2 ?k)) (when (= ?i 1) (assign ?v1 (+ ?v1 ?k))) (when (= ?i 3) (assign ?v3 (+ ?v3 ?k)))))
    (:action take3
        :parameters (?k ?i)
        :precondition (or (and (= ?i 1) (> ?v3 ?v1) (> ?k 0) (> (- ?v3 ?v1) ?k)) (and (= ?i 2) (> ?v3 ?v2) (> ?k 0) (> (- ?v3 ?v2) ?k)))
        :effect (and (assign ?v3 (- ?v3 ?k)) (when (= ?i 1) (assign ?v1 (+ ?v1 ?k))) (when (= ?i 2) (assign ?v2 (+ ?v2 ?k)))))
)