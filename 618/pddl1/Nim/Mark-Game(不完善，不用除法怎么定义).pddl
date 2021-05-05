(define (domain  Mark-Game)
	(:objects ?v)
	(:tercondition (= ?v 0))
    (:constraint (>= ?v 0))
    (:action take1
        :parameters (?k)
        :precondition (and (= 1 ?k) (> ?v 0))
        :effect (assign ?v (- ?v ?k)))
    (:action take2
        :parameters (?k)
        :precondition (and (or (and () ()) ()) (> ?v 1))
        :effect (assign ?v (- ?v ?k)))
)