;honeycomb2.ctl file for triangular lattice but of full honeycombs

(set! num-bands 6) ;set num bands
(define-param r 0.125) ;2r is the same as hole_size
(define-param eps 1) ;eps for the holes, should be air
(define-param h 0) 
(set! h (* r (sqrt 3))) ;forces equilateral triangle
(define-param a 1) ;everything is now in units of a
(define-param R 0)

(define-param rfrac 1.1) ; define rfrac here!!!
(set! R (/ 1 3)) ;R defaults to a over 3

(set! R (* R rfrac)) ;re-sets R to R*rfrac since Rfrac is the ratio of real R to a/3


(set! default-material (make dielectric (epsilon 2.2))) ;set dielectric of material

(set! geometry-lattice (make lattice (size a a no-size)
						(basis1 0.5 (/ (sqrt 3) 2) ) ;triangular lattice basis
						(basis2 0.5 (/ (sqrt 3) -2) )))



;hexagonal coordinates in new basis
(define-param center1 (vector3 (* R 1) (* R 1) 0))
(define-param center2 (vector3 (* R 1) (* R 0) 0))
(define-param center3 (vector3 (* R 0) (* R -1) 0))
(define-param center4 (vector3 (* R -1) (* R -1) 0))
(define-param center5 (vector3 (* R -1) (* R 0) 0))
(define-param center6 (vector3 (* R 0) (* R 1) 0))

;construct 6 cones, on side (axis defined by the negative of the vector to the center)

(set! geometry (list (make cone
						(center center1) (radius r) (height h) (axis center4)
						(material (make dielectric (epsilon eps))))
					 (make cone
						(center center2) (radius r) (height h) (axis center5)
						(material (make dielectric (epsilon eps))))
					 (make cone
						(center center3) (radius r) (height h) (axis center6)
						(material (make dielectric (epsilon eps))))
					 (make cone
						(center center4) (radius r) (height h) (axis center1) 
						(material (make dielectric (epsilon eps))))
					 (make cone
						(center center5) (radius r) (height h) (axis center2)
						(material (make dielectric (epsilon eps))))
					 (make cone
						(center center6) (radius r) (height h) (axis center3)
						(material (make dielectric (epsilon eps))))))


;define the hexagonal brillouin zone
(set! k-points (list (vector3 (/ 1 3) .57735 0) ;K point.
						(vector3 0 0 0) ;gamma 
						(vector3 0 .57735 0) ; M 
						(vector3 (/ 1 3) .57735 0))) ; K


(set! k-points (interpolate 20 k-points)) ;set number of points between each major K point, this must be matched in python code if changed

(set! resolution 64) ;resolution for dielectric I think, match in python code, pixels per lattice unit

;(run-tm (output-at-kpoint (vector3 (/ -3) (/ 3) 0)
;							fix-efield-phase output-efield-z))
(run-tm)
(run-te)