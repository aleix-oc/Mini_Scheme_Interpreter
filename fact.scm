(define (factorial n)
    (if (= n 1)
        1
        (* n (factorial (- n 1)))))

; Retorna llista amb els factorials de n a 1
(define (llista_factorial n)
    (if (= n 0)
        '()
        (cons (factorial n) (llista_factorial (- n 1)))))

; Filter clàssic
(define (filter pred l)
    (cond
        ((null? l) '())
        ((pred (car l)) (cons (car l) (filter pred (cdr l))))
        (#t (filter pred (cdr l)))))

;Comptem dígits
(define (digits x)
    (if (< x 10)
        1
        (+ 1 (digits (/ x 10)))))

(define (div_digits x)
    (not(= (mod (digits x) 2) 0)))

; Entrada de dades
(define (main)
    (display "Factorials de n a 0") (newline)
    (display "Introdueixi un nombre natural: ")
    (let ((n (read)))
        (display "Llista de factorials:")
        (let ((facts (llista_factorial n)))
        (display facts) (newline)
        (display "Filtrem els que tinguin nombre senar de dígits:") (newline)
        (display (filter div_digits facts)))))
