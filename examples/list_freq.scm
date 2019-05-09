#!/usr/bin/env slyther
(define list-1 '(12 3 4 5 6 8 19 202 30 40 3 3))
(define list-2 '("hello" "hello" "world" "this" "is" "d6" "lisp_eval"
                 "lisp"))
(define list-3 '())
(define list-4 '(#t #t #t #f #f #t #f))

(define target-1 '(12 3 4 5))
(define target-2 '("hello" "world" "lisp"))
(define target-3 '(12 3 4 5))
(define target-4 '(#t #f))
(define target-5 '())

(print "for '(12 3 4 5 6 8 19 202 30 40 3 3) as input and target '(12 3 4 5)")
(print "output is : ")
(print (list-frequency list-1 target-1))
(print "should be : (list (list 12 1) (list 3 3) (list 4 1) (list 5 1))\n")

(print "for '(\"hello\" \"hello\" \"world\" \"this\" \"is\" \"d6\" \"lisp_eval\"\"lisp\") as input and target '(\"hello\" \"world\" \"lisp\")")
(print "output is : ")
(print (list-frequency list-2 target-2))
(print "should be : (list (list \"hello\" 2) (list \"world\" 1) (list \"lisp\" 1))\n")

(print "for '() as input and target  '(12 3 4 5)")
(print "output is : ")
(print (list-frequency list-3 target-3))
(print "should be : (list (list 12 0) (list 3 0) (list 4 0) (list 5 0))\n")

(print "for '(#t #t #t #f #f #t #f) as input and target  '(#t #f)")
(print "output is : ")
(print (list-frequency list-3 target-4))
(print "should be : (list (list #t 4) (list #f 3))\n")

(print "for '(12 3 4 5 6 8 19 202 30 40 3 3) as input and target  '()")
(print "output is : ")
(print (list-frequency list-3 target-5))
(print "should be : NIL\n")