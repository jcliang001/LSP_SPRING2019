import operator
from functools import reduce
from slyther.types import (BuiltinFunction, BuiltinMacro, Symbol,
               UserFunction, SExpression, cons, String,
               ConsList, NIL, LexicalVarStorage, ConsCell,
               Variable)
from slyther.evaluator import lisp_eval
from slyther.parser import lex, parse
from math import floor, ceil, sqrt


@BuiltinFunction('+')
def add(*args):
  """
  Sum each of the arguments

  >>> add(1, 2, 3, 4)
  10
  >>> add()
  0

  .. hint::

    Use ``sum`` or ``reduce``.
  """

  return reduce(lambda x, y: x + y, args, 0)

  # raise NotImplementedError("Deliverable 3")


@BuiltinFunction('-')
def sub(*args):
  """
  ``(- x y z)`` computes ``x - y - z``, but with only one argument,
  ``(- x)`` computes ``-x``.

  >>> sub(10, 1, 2)
  7
  >>> sub(10, 1)
  9
  >>> sub(10)
  -10
  >>> sub()
  0

  .. hint::

    Use ``reduce``.
  """
  if(len(args) == 0):
    return 0
  if(len(args) == 1):
    return args[0] * -1
  return reduce(lambda x, y: x - y, args)

  # raise NotImplemntdError("Deliverable 3")


@BuiltinFunction('*')
def mul(*args):
  """
  Compute the product.

  >>> mul(2, 3)
  6
  >>> mul(2, 3, 3)
  18
  >>> mul(2)
  2
  >>> mul()
  1
  """

  return reduce(lambda x, y: x * y, args, 1)
  # raise NotImplementedError("Deliverable 3")


@BuiltinFunction('/')
def div(*args):
  """
  ``(/ a b c)`` computes ``a / b / c``, but ``(/ a)`` computes
  ``1 / a``.

  >>> div(1, 2)
  0.5
  >>> div(1, 2, 2)
  0.25
  >>> div(2)
  0.5
  """
  if(len(args) == 1):
    return 1 / args[0]
  return reduce(lambda x, y: x / y, args)

  # raise NotImplementedError("Deliverable 3")


@BuiltinFunction
def floordiv(*args):
  """
  Equivalent to ``div``, but uses ``operator.floordiv``.

  >>> floordiv(3, 2)
  1
  >>> floordiv(3, 2, 2)
  0
  >>> floordiv(1)
  1
  >>> floordiv(2)
  0
  """

  if(len(args) == 1):
    return 1 // args[0]
  return reduce(operator.floordiv, args)
  # raise NotImplementedError("Deliverable 3")


# IO
print_ = BuiltinFunction(print)
input_ = BuiltinFunction(input)

# Type Constructors
make_int = BuiltinFunction(int, 'make-integer')
make_float = BuiltinFunction(float, 'make-float')
make_symbol = BuiltinFunction(Symbol, 'make-symbol')
make_string = BuiltinFunction(String, 'make-string')


@BuiltinFunction('list')
def list_(*args) -> ConsList:
  """
  Create a ``ConsList`` from ``args``.

  >>> list_(1, 2, 3)
  (list 1 2 3)
  >>> list_()
  NIL
  """
  if(len(args) == 0):
    return NIL
  x = range(len(args) - 2, -1, -1)
  ret_list = ConsList(args[len(args) - 1])
  for i in x:
    ret_list = cons(args[i], ret_list)
  return ret_list
  # raise NotImplementedError("Deliverable 3")


# Comparators
lt = BuiltinFunction(operator.lt, '<')
gt = BuiltinFunction(operator.gt, '>')
eq = BuiltinFunction(operator.eq, '=')
le = BuiltinFunction(operator.le, '<=')
ge = BuiltinFunction(operator.ge, '>=')
not_ = BuiltinFunction(operator.not_, 'not')

# arithmetic
remainder = BuiltinFunction(operator.mod, 'remainder')
floor_ = BuiltinFunction(floor)
ceil_ = BuiltinFunction(ceil)
sqrt_ = BuiltinFunction(sqrt)
abs_ = BuiltinFunction(abs)
expt = BuiltinFunction(operator.pow, 'expt')

# string manipulation
format_ = BuiltinFunction(str.format)
split = BuiltinFunction(str.split)

# cons cell functions
cons = BuiltinFunction(cons)


@BuiltinFunction
def car(cell: ConsCell):
  """
  Get the ``car`` of a cons cell.
  """

  return cell.car
  # raise NotImplementedError("Deliverable 3")


@BuiltinFunction
def cdr(cell: ConsCell):
  """
  Get the ``cdr`` of a cons cell.
  """
  return cell.cdr
  # raise NotImplementedError("Deliverable 3")


@BuiltinFunction('nil?')
def is_nil(cell: ConsCell) -> bool:
  """
  Return ``True`` if the cell is ``NIL``, ``False`` otherwise.
  """

  if cell is NIL:
    return True
  return False
  # raise NotImplementedError("Deliverable 3")


@BuiltinMacro
def define(se: SExpression, stg: LexicalVarStorage):
  """
  Define a variable or a function to a value, calling ``put`` on
  the storage::

    ; variable
    (define var-name evaluate-me)

    ; lambda function
    (define func-name (lambda (args...) (body1) ... (bodyN)))

    ; SE-named function
    (define (func-name args...) (body1) ... (bodyN))

  .. note::

    If defining a function (either by ``lambda`` or by SE-named
    syntax), the definition **must** be made visible from within
    that function's ``environ``, or recursion will not work!

  >>> from slyther.types import *
  >>> from slyther.parser import lisp
  >>> se = lisp('((twirl alpha beta) (print alpha) (print beta))')
  >>> name = Symbol('twirl')
  >>> args = lisp('(alpha beta)')
  >>> body = lisp('((print alpha) (print beta))')
  >>> stg = LexicalVarStorage({})
  >>> stg.put('NIL', NIL)
  >>> stg.put('define', define) # so that you can return a define if you want
  >>> stg.put('lambda', lambda_func)
  >>> from slyther.evaluator import lisp_eval
  >>> lisp_eval(define(cons(cons(name, args), body), stg), stg)
  NIL
  >>> lisp_eval(define(lisp('(x 10)'), stg), stg)
  NIL
  >>> stg[name].value
  (lambda (alpha beta) (print alpha) (print beta))
  >>> stg[name].value.environ['twirl'].value
  (lambda (alpha beta) (print alpha) (print beta))
  >>> stg['x'].value
  10
  >>> stg[name].value.environ['x'].value
  Traceback (most recent call last):
    ...
  KeyError: 'x'
  """
  # raise NotImplementedError("Deliverable 4")
  key = se.car
  value = se.cdr

  if isinstance(key, SExpression):
    function = UserFunction(params=key.cdr, body=value, environ=stg.fork())
    key = key.car
    function.environ[key] = Variable(function)
    stg.put(key, function)
  elif isinstance(se.car, Symbol):
    stg.put(key, lisp_eval(value.car, stg))
  else:
    stg.put(key, value)


@BuiltinMacro('lambda')
def lambda_func(se: SExpression, stg: LexicalVarStorage) -> UserFunction:
  """
  Define an anonymous function and return the ``UserFunction``
  object.

  >>> from slyther.types import *
  >>> stg = LexicalVarStorage({})
  >>> stg.put('x', 20)
  >>> f = lambda_func(
  ...     SExpression.from_iterable([
  ...         SExpression.from_iterable(map(Symbol, ['a', 'b', '.', 'c'])),
  ...         SExpression.from_iterable(map(Symbol, ['print', 'a'])),
  ...         SExpression.from_iterable(map(Symbol, ['print', 'b'])),
  ...         SExpression.from_iterable(map(Symbol, ['print', 'c']))]),
  ...     stg)
  >>> f
  (lambda (a b . c) (print a) (print b) (print c))
  >>> f.environ['x'].value
  20
  """
  return UserFunction(se.car, se.cdr, stg.fork())
  # raise NotImplementedError("Deliverable 4")


@BuiltinMacro('let')
def let(se: SExpression, stg: LexicalVarStorage) -> SExpression:
  """
  The ``let`` macro binds variables to a local scope: the expressions
  inside the macro. Like a function, a ``let`` returns the last
  expression in its body. Once the ``let`` returns, the variables are
  unbound, and cannot be accessed anymore. For example::

    (let ((a (+ f g))
        (b 11)
        (c 12))
      (+ a (- b c)))

  In the example above, ``a`` was bound to whatever ``(+ f g)``
  evaluates to, b to ``11``, and ``c`` to ``12``.

  Notice how the above was equivalent to another expression::

    ((lambda (a b c) (+ a (- b c))) (+ f g) 11 12)

  You should do a syntax translation from the input to something like that.

  >>> from slyther.types import *
  >>> from slyther.parser import lisp
  >>> from slyther.evaluator import lisp_eval
  >>> stg = LexicalVarStorage(
  ...         {'let': Variable(let),
  ...          'lambda': Variable(lambda_func),
  ...          'print': Variable(print_),
  ...          'x': Variable(10)})
  >>> lisp_eval(lisp('(let ((x 20) (y 30)) (print x) (print y))'), stg)
  20
  30
  NIL
  >>> lisp_eval(Symbol('x'), stg)
  10
  """
  # raise NotImplementedError("Deliverable 4")

  # stg_copy = stg
  # params = []
  # body = []
  # variables = []

  # for l in se.car:
  #     params.appenLexicalVarStoraged(Symbol(l.car))
  #     variables.append(lisp_eval(l.cdr.car, stg))
  #     # print(l.car, ", ", l.cdr.car)
  #     stg.put(l.car, lisp_eval(l.cdr.car, stg))

  # for l in se.cdr:
  #     body.append(Symbol(l))
  #     print(l)
  #     # lisp_eval(l, stg)

  # params = SExpression.from_iterable(params)
  # variables = SExpression.from_iterable(variables)
  # # body.append(variables)
  # body = SExpression.from_iterable(body)

  # l = UserFunction(params=params,body=body,environ=stg.fork())
  # print(variables)
  # return l(*variables)

  stg_copy = LexicalVarStorage(stg.fork())

  for l in se.car:
    stg_copy.put(l.car, lisp_eval(l.cdr.car, stg_copy))

  ret = None
  for l in se.cdr:
    ret = lisp_eval(l, stg_copy)

  # stg = stg_copy
  return ret


@BuiltinMacro('if')
def if_expr(se: SExpression, stg: LexicalVarStorage):
  """
  An ``if`` expression looks like this::

    (if <predicate> <consequent> <alternative>)

  If the predicate evaluates to something truthy, return the
  consequent, otherwise return the alternative. An example::

    (if (< x 10)
      (print "x is less than 10")
      (print "x is greater than or equal to 10"))

  >>> from slyther.types import *
  >>> from slyther.parser import lisp
  >>> se = lisp('((< x 10)'
  ...           ' (print "x is less than 10")'
  ...           ' (print "x is greater than or equal to 10"))')
  >>> stg = LexicalVarStorage({})
  >>> stg.put('<', lt)
  >>> stg.put('x', 9)
  >>> if_expr(se, stg)
  (print "x is less than 10")
  >>> stg['x'].set(10)
  >>> if_expr(se, stg)
  (print "x is greater than or equal to 10")
  """

  if(lisp_eval(se.__getitem__(0), stg)):
    return se.__getitem__(1)
  return se.__getitem__(2)
  # raise NotImplementedError("Deliverable 4")


@BuiltinMacro('cond')
def cond(se: SExpression, stg: LexicalVarStorage):
  """
  ``cond`` is similar to ``if``, but it lists a series of predicates
  and consequents, similar to how guards work in Haskell. For
  example::

    (cond
      ((< x 5) (print "x < 5"))
      ((< x 10) (print "5 <= x < 10"))
      ((< x 15) (print "10 <= x < 15"))
      (#t (print "x >= 15")))

  >>> from slyther.types import *
  >>> from slyther.parser import lex, parse
  >>> def test_cond(x):
  ...     expr = next(parse(lex('''
  ...         (ifcond
  ...           ((< x 5) (print "x < 5"))
  ...           ((< x 10) (print "5 <= x < 10"))
  ...           ((< x 15) (print "10 <= x < 15"))
  ...           (#t (print "x >= 15")))''')))
  ...     stg = LexicalVarStorage({})
  ...     stg.put('<', lt)
  ...     stg.put('#t', Boolean(True))
  ...     stg.put('x', x)
  ...     return cond(expr.cdr, stg)
  >>> test_cond(4)
  (print "x < 5")
  >>> test_cond(5)
  (print "5 <= x < 10")
  >>> test_cond(10)
  (print "10 <= x < 15")
  >>> test_cond(15)
  (print "x >= 15")
  """

  index = 0
  while(index < se.__len__()):
    if(lisp_eval(se.__getitem__(index).__getitem__(0), stg)):
      return se.__getitem__(index).__getitem__(1)
    index += 1

  # raise NotImplementedError("Deliverable 4")


@BuiltinMacro('and')
def and_(se: SExpression, stg: LexicalVarStorage):
  """
  Compute an ``and`` expression, like this::

    (and (< x 10) (> y 15) (foo? z))

  Evaluate left to right, and return the first result which produces
  a falsy value. Note that the result need not be a boolean, but you
  should test its falsiness, and return the result (even if it's not
  a boolean).

  Note that you could return the last expression unevaluated if all
  the previous are truthy, as your ``lisp_eval`` should eval it for
  you. This could be useful for tail call optimization.

  >>> from slyther.types import *
  >>> from slyther.parser import lisp
  >>> from slyther.evaluator import lisp_eval
  >>> stg = LexicalVarStorage(
  ...         {'and': Variable(and_),
  ...          '#f': Variable(Boolean(False)),
  ...          '#t': Variable(Boolean(True)),
  ...          'print': Variable(print_),
  ...          '+': Variable(add),
  ...          'x': Variable(0),
  ...          'y': Variable(1),
  ...          'z': Variable(2)})
  >>> lisp_eval(lisp('(and #t (print (+ x y z)) #f)'), stg)
  3
  NIL
  >>> lisp_eval(lisp('(and #f (print (+ x y z)) #f)'), stg)
  #f
  >>> lisp_eval(lisp('(and #t x (print (+ x y z)) y foo)'), stg)
  0
  >>> lisp_eval(lisp('(and (+ x y) y z)'), stg)
  2
  >>> lisp_eval(lisp('(and)'), stg)
  NIL
  """

  index = 0
  result = NIL
  while(index < se.__len__()):
    if(se.__getitem__(index) == '#f'):
      return False
    result = lisp_eval(se.__getitem__(index), stg)
    if(not result):
      return result
    index += 1
  return result
  # raise NotImplementedError("Deliverable 4")


@BuiltinMacro('or')
def or_(se: SExpression, stg: LexicalVarStorage):
  """
  Similar to ``and`` above, but compute an ``or`` instead. Return
  the first truthy value rather than falsy.

  >>> from slyther.types import *
  >>> from slyther.parser import lisp
  >>> from slyther.evaluator import lisp_eval
  >>> stg = LexicalVarStorage(
  ...         {'or': Variable(or_),
  ...          '#f': Variable(Boolean(False)),
  ...          '#t': Variable(Boolean(True)),
  ...          'print': Variable(print_),
  ...          '+': Variable(add),
  ...          'x': Variable(0),
  ...          'y': Variable(1),
  ...          'z': Variable(2)})
  >>> lisp_eval(lisp('(or #t (print (+ x y z)) #f)'), stg)
  #t
  >>> lisp_eval(lisp('(or #f (print (+ x y z)) #f)'), stg)
  3
  #f
  >>> lisp_eval(lisp('(or #f x (print (+ x y z)) y foo)'), stg)
  3
  1
  >>> lisp_eval(lisp('(or (+ y -1) x z)'), stg)
  2
  >>> lisp_eval(lisp('(or)'), stg)
  NIL
  """

  index = 0
  result = NIL
  while(index < se.__len__()):
    if(se.__getitem__(index) == '#t'):
      return True
    result = lisp_eval(se.__getitem__(index), stg)
    if(result):
      return result
    index += 1
  return result
  # raise NotImplementedError("Deliverable 4")


@BuiltinMacro('set!')
def setbang(se: SExpression, stg: LexicalVarStorage):
  """
  ``set!`` is the assigment macro. Unlike ``define``, ``set!`` **does not
  create new variables.** Instead, it changes the value of existing
  variables **only**. If given a variable which has not been defined,
  it should raise a ``KeyError``.

  For example::

    (set! <name> <value>)

  Should just eval ``value`` and call ``stg[name].set`` on it. Return
  ``NIL``.

  >>> from slyther.types import *
  >>> from slyther.parser import lisp
  >>> stg = LexicalVarStorage({'foo': Variable(12), 'bar': Variable(15)})
  >>> old_foo = stg['foo']
  >>> setbang(lisp('(foo 15)'), stg)
  NIL
  >>> stg['foo'].value
  15
  >>> stg['foo'] is old_foo
  True
  >>> setbang(lisp('(baz 15)'), stg)
  Traceback (most recent call last):
    ...
  KeyError: 'Undefined variable baz'
  """
  try:
    stg[se.car].set(lisp_eval(se.cdr.car, stg))
    return NIL
  except KeyError:
    raise KeyError("Undefined variable " + str(se.car))

  # raise NotImplementedError("Deliverable 4")


@BuiltinMacro('eval')
def eval_(se: SExpression, stg: LexicalVarStorage):
  """
  ::

    (eval <expr>)

  Evaluate ``expr``, if it produces a ``ConsList``, then upgrade that
  ``ConsList`` to an ``SExpression`` (recursively) and return it. Your
  ``lisp_eval`` will take care of actually evaluating the expression,
  as this is a macro.

  >>> from slyther.types import *
  >>> from slyther.parser import lisp
  >>> from slyther.evaluator import lisp_eval
  >>> stg = LexicalVarStorage(
  ...         {'eval': Variable(eval_),
  ...          '#t': Variable(Boolean(True)),
  ...          'print': Variable(print_),
  ...          'x': Variable(0),
  ...          'y': Variable(1),
  ...          'z': Variable(lisp("(print x)"))})
  >>> lisp_eval(lisp("(eval '(print x))"), stg)
  0
  NIL
  >>> lisp_eval(lisp("(eval ''(print x))"), stg)
  (list print x)
  >>> lisp_eval(lisp('(eval #t)'), stg)
  #t
  >>> lisp_eval(lisp("(eval '''#t)"), stg)
  '#t
  >>> lisp_eval(lisp("(eval 'y)"), stg)
  1
  >>> lisp_eval(lisp("(eval ''y)"), stg)
  y
  >>> lisp_eval(lisp("(eval z)"), stg)
  0
  NIL
  """

  le = lisp_eval(se.car, stg)

  # if se.cdr is NIL:
  #     #print("")
  #     #return lisp_eval(se.car, stg)
  #     return NIL

  if isinstance(le, ConsList):
    return lisp_eval(SExpression.from_iterable(le), stg)

  return le
  # eval_se = lisp_eval(se.cdr, stg)

  # if isinstance(eval_se, ConsList):
  #     print(SExpression.from_iterable(lisp_eval(se.cdr, stg)))
  #     eval_(SExpression.from_iterable(lisp_eval(se.cdr, stg)), stg)
  # else:
  #     return se

  # raise NotImplementedError("Deliverable 4")


@BuiltinFunction('parse')
def parse_string(code: String):
  """
  ``code`` is a ``String`` containing a single thing once parsed, such as an
  s-expression, or a symbol. Simply just lex it, parse it and return it!
  Woo-hoo!

  >>> from slyther.types import *
  >>> parse_string(String("(print x)"))
  (list print x)

  Note that the ``BuiltinFunction`` decorator takes care of downgrading an
  ``SExpression`` to a ``ConsList`` for you.
  """
  # raise NotImplementedError("Deliverable 4")

  return next(parse(lex(code)))

@BuiltinFunction('require')
def require(library: String):
  try:
    import library
  except ImportError:
    raise ImportError("No library named {} found".format(library))
