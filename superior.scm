; Constant per si es vol usar per veure que l'ús de constants funciona perfectament
; S'ha de fer replace d'aux per "llisteta", substitueix a la segona llista d'entrada
(define llisteta '(1 2 3))

(define (foldl f acc l)
  (if (null? l)
      acc
      (foldl f (f acc (car l)) (cdr l))))

;Encapsulament d'aritmetques
(define (suma x y) (+ x y))

(define (square x) (* x x))

(define (map f l)
    (if (null? l)
        '()
        (cons (f (car l)) (map f (cdr l)))))

(define (zip l aux)
    (cond
        ((and (null? l) (null? aux)) '())
        ((and (null? l) (not (null? aux))) l)
        ((and (null? aux) (not (null? l))) aux)
        (#t (cons (car l) (cons (car aux) (zip (cdr l) (cdr aux)))))))

; Proves amb llistes
(define (main) (display "Introdueix una llista de nombres: ")
  (let ((llista (read)))

    (display "Primer element de la llista: ") (display (car llista)) (newline)
    (display "Cua de la llista: ") (display (cdr llista)) (newline)

    (display "Suma de elements de la llista: ")
    (display (foldl suma 0 llista)) (newline)


    (display "Elevar llista al quadrat:")
    (display (map square llista)) (newline)

    (display "Zipeja amb una altra llista (admet multi-tipus):"); Funciona amb llistes multi-tipus
    (display (zip llista (read)))
    (newline)))
