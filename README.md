ika
==========

Yet another LISP Interpreter.

## Progress

### DONE

- Fake compiler.
- Lambda function and Function apply.
- `begin`, `set!`
- Closure and Lexical scope.
- `call/cc` and Tail recursion optimization.

### TODO

- macro
- if, car, cdr, cons, pair?, atom?, ...


## Example
```Scheme
(define a (lambda () (a)))
(a)
```

```Scheme
(define f (lambda (return) (return 2) 3))
(f (lambda (x) x)) ; => 3
(call/cc f) ; => 2
```
