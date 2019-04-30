from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

def repl(interpreter, debug=False):
    """
    Take an interpreter object (see ``slyther/interpreter.py``) and give a REPL
    on it. Should not return anything: just a user interface at the terminal.
    For example::

        $ slyther
        > (print "Hello, World!")
        Hello, World!
        NIL
        > (+ 10 10 10)
        30

    When the user presses ^D at an empty prompt, the REPL should exit.

    When the user presses ^C at any prompt (whether there is text or
    not), the input should be cancelled, and the user prompted again::

        $ slyther
        > (blah bla^C
        >                   <-- ^C resulted in new prompt line

    Should be pretty easy. No unit tests for this function, but I will
    test the interface works when I grade it.

    Optionally, you may want to prevent the REPL from raising an exception
    when an exception in user code occurs, and allow the user to keep
    typing further expressions. This is not required, just a suggestion.
    If you do this, you should probably disable this behavior when ``debug``
    is set to ``True``, as it allows for easy post-mortem debugging with pdb
    or pudb.
    """
    # Word completer from slyther.builtins.py
    slyther_completer = WordCompleter([
        'abs', 'and', 'car', 'cdr', 'ceil', 'cond', 'cons', 'define', 'eval', 'expt', 'floor', 'floordiv', 'if', 'input', 'lambda', 'let', 'list', 'make-float', 'make-integer', 'make-string', 'make-symbol', 'not', 'or', 'remainder', 'parse', 'print', 'set!', 'sqrt'], ignore_case=True)

    while True:
        try:
            expr = prompt('>',
                          history=FileHistory('history.txt'),
                          auto_suggest=AutoSuggestFromHistory(),
                          completer=slyther_completer)
            print(interpreter.exec(expr))
        except KeyboardInterrupt:
            print("")
            continue
        except EOFError:
            exit(0)
