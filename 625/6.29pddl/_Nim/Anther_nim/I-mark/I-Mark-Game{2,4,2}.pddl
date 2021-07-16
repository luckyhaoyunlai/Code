(define (domain  i-mark-Game)
	(:objects ?v1)
	(:tercondition (<  ?v1 2))
    (:constraint (>= ?v1 0))
    (:action take1
        :parameters (?k)
        :precondition (and (or (= ?k 2)  (= ?k 4))  (> ?v1 ?k))
        :effect (assign ?v1 (- ?v1 ?k)))
    (:action take2
        :parameters (?k)
        :precondition (and (= ?v1 (+ ?k ?k)) (> ?v1 ?k))
        :effect (assign ?v1  ?k))
)