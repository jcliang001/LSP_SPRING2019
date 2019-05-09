import operator
from functools import reduce
from slyther.types import (BuiltinFunction, BuiltinMacro, Symbol,
                           UserFunction, SExpression, cons, String,
                           Variable, ConsList, NIL, LexicalVarStorage,
                           ConsCell)
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
    return sum(args)


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
    if len(args) == 1:
        return -1 * args[0]
    if len(args) > 1:
        return reduce(lambda x, y: x - y, args)
    else:
        return 0


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
    product = 1
    for i in args:
        product *= i
    return product


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
    if len(args) == 1:
        return operator.truediv(1, args[0])
    if len(args) > 1:
        return reduce(lambda x, y: operator.truediv(x, y), args)
    else:
        return 0


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
    if len(args) == 1:
        return operator.floordiv(1, args[0])
    if len(args) > 1:
        return reduce(lambda x, y: operator.floordiv(x, y), args)
    else:
        return 0


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
    return ConsList.from_iterable(args)


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


@BuiltinFunction
def cdr(cell: ConsCell):
    """
    Get the ``cdr`` of a cons cell.
    """
    return cell.cdr


@BuiltinFunction('nil?')
def is_nil(cell: ConsCell) -> bool:
    """
    Return ``True`` if the cell is ``NIL``, ``False`` otherwise.
    """
    return cell.car == NIL


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
    >>> stg.put('define', define)
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
    key = se.car
    value = se.cdr

    if isinstance(key, SExpression):
        function = UserFunction(params=key.cdr, body=value, environ=stg.fork())
        key = key.car
        function.environ[key] = Variable(function)
        stg.put(key, function)
    elif isinstance(key, Symbol):
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

        ((lambda (a b c)
           (+ a (- b c))) (+ f g) 11 12)

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
    vals = []
    ptrs = []
    pred = se.car
    con = se.cdr
    for item in pred:
        vals.append(item.car)
        ptrs.append(item.cdr.car)
    param = SExpression.from_iterable(vals)
    ptrs = SExpression.from_iterable(ptrs)
    function = UserFunction(params=param, body=con, environ=stg.fork())
    res = SExpression(function, ptrs)

    return res


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
    if lisp_eval(se.car, stg):
        return se.cdr.car
    else:
        return se.cdr.cdr.car


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
    ...         (cond
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
    while se is not NIL:
        if(lisp_eval(se.car.car, stg)):
            return se.car.cdr.car
        se = se.cdr


@BuiltinMacro('and')
def and_(se: SExpression, stg: LexicalVarStorage):
    """
    Compute an ``and`` expression, like this::

        (and (< x 10) (> y 15) (foo? z))

    Evaluate left to right, and return the first result which produces
    a falsy value. Note that the result need not be a boolean, but you
    should test its falsiness(parse(lex('''
    ...         (cond
    ...           ((< x 5) (print "x < 5"))
    ...           ((< x 10) (print "5 <= x < 10"))
    ...           ((< x 15) (print "10 <= x < 15"))
    ...           (#t (print "x >= 15")))'''))), and return the result (even if it's not
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
    res = NIL
    length = len(se)
    for index, x in enumerate(se):
        if index == length - 1:
            return x
        y = lisp_eval(x, stg)
        res = y
        if not y:
            return y
    return res


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
    res = NIL
    length = len(se)
    for index, x in enumerate(se):
        if index == length - 1:
            return x
        y = lisp_eval(x, stg)
        res = y
        if y:
            return y
    return res

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
    except KeyError as ex:
        raise KeyError("Undefined variable {}".format(str(se.car))) from ex


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
    expression = lisp_eval(se.car, stg)
    if isinstance(expression, ConsList):
        expression = SExpression.from_iterable(
            eval_(SExpression(x), stg) for x in expression)

    return expression


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
    return next(parse(lex(code)))

# Given an input list, we will count the frequency from the members in the
# target list.
@BuiltinFunction('list-frequency')
def list_frequency(input_list: SExpression, target_list: SExpression):
    """
    $slyther
    >(list_frequency '(12 2 3 3 2 3 2 2 22 12 4 12) '(12 2 3 4))
    (list (list 12 3) (list 2 4) (list 3 3) (list 4 1))

    """
    
    # create an map that stores all the elements from input_list
    table = {}
    while input_list is not NIL:
        key = input_list.car
        if key in table:
            table[key] += 1
        else:
            table[key] = 1
        
        input_list = input_list.cdr

    root = ConsList(0, NIL)
    res = root
    check = 0
    size = len(target_list)

    if size == 0:
        return NIL

    # delete the keys that are not in the input list 
    while target_list is not NIL:
        check += 1
        key = target_list.car
        if key in table:
            value = table[key]
            root.car = ConsList(key, NIL)
            root.car.cdr = ConsList(value, NIL)
        else:
            root.car = ConsList(key, NIL)
            root.car.cdr = ConsList(0, NIL)
        if check != size:
            root.cdr = ConsList(0, NIL)
            root = root.cdr
        
        target_list = target_list.cdr
    
    # generate the result:

    return res


