(define saluda "hola món!")

(define (fibonacci x y z)
  (if (= z 0)
    x
    (fibonacci y (+ x y) (- z 1))))

(define (es-senar x)
  (not (= (mod x 2) 0)))

(define (procesar x)
  (cond
    ((es-senar x) "senar")
    (#t "parell")))

; Testegem condicions
(define (logica a b)
  (if (and (> a b) (es-senar b))
      (* a b)
      (+ a b)))

(define (main)
  (display saluda) (newline)

  (display "Procesa un número de entrada: ")
  (display (procesar (read))) (newline)

  (display "Introdueixi dos nombres, si el segon es senar i menor multipliquem, altrament sumem: ")
  (display (logica (read) (read))) (newline)

  (display "Fibonacci de n: ")
  (display (fibonacci 0 1 (read))) (newline))
