(define (domain chomp-game)
    (:objects ?v1 ?v2)
    (:tercondition (= (+ ?v1 ?v2) 1))
    (:constraint (and (>= ?v1 1) (>= ?v2 1) (!= (+ ?v1 ?v2) 0)))
    (:action move1
        :parameters (?k)
        :precondition (and (>= ?v1 ?k) (> ?k 0))
        :effect (and  (assign ?v1 (- ?v1 ?k)) (assign ?v2 (+ ?v2 ?k))))
    (:action move2
        :parameters (?k)
        :precondition (and (>= ?v2 ?k) (> ?k 0))
        :effect (assign ?v2 (- ?v2 ?k)))
    (:action move3
        :parameters (?k)
        :precondition (and (>= ?v1 ?k) (> ?k 0))
        :effect (and  (assign ?v1 (- ?v1 ?k)) (assign ?v2 0)))
)
