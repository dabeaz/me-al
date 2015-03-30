'''
Meẗal - Better Than Decoration

Synopsis
========
So, you've fully explored the use of decorators and maybe even
decorators with arguments.  Where do you go from there?  Where you
ask?  You, my friend, need to apply Meẗal--the better decorator.

For example, here is a function:

    # simple.py
    def hello(name):
        print('Hello', name)

Here is the same function with some Meẗal indicated:

    # simple.py

    def ḧellö(name):
        print('Hello', name)

The only remaining step is for you to apply the kind of metal you
desire.  This is done using a standard decorator function:

    # example.py
    import meẗal

    # A decorator (aka., "the meẗal")
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("Decorator")
            return func(*args, **kwargs)
        return wrapper

    # Apply the meẗal to the module
    with meẗal(decorator):
        import simple

    # Call the module with the meẗal applied
    simple.hello('Guido')

Now, run your program:

    bash % python3 example.py
    Decorator
    Hello Guido
    bash %

You'll see your decorator applied to the functions requesting
meẗal. If the above command fails with an ImportError, you're probably
using a Mac. That's an unfortunate choice as you can't really expect a
machine like that to be used for serious tasks.  Nevertheless, if
you'd really like to apply meẗal anyways, you can still do it by
changing the top level import to the following:

    # example.py
    meẗal = __import__('met\u0308al')
    ...

Although, for maximum portability, I'd suggest the following:

    try:
        import meẗal
    except ImportError:
        meẗal = __import__('met\u0308al')

Closer to the Meẗal
===================
Our simple example was really just a small taste to get the idea. If
you really want to get serious though, you can use Meẗal with a
package such as Numba:

    import meẗal
    from numba import jit

    with meẗal(jit):
        import simple

Now, you're starting to get the idea.

Meẗal is Different
==================
Meẗal allows different decorators to be applied to the same module on
different import statements--even in the same file!  Observe:

    def decorator1(func):
        def wrapper(*args, **kwargs):
            print("Decorator 1")
            return func(*args, **kwargs)
        return wrapper

    def decorator2(func):
        def wrapper(*args, **kwargs):
            print("Decorator 2")
            return func(*args, **kwargs)
        return wrapper

    # Use a module with decorator1 meẗal applied
    with meẗal(decorator1):
        import simple
        simple.hello('Guido')

    # Use a module with decorator2 meẗal applied
    with meẗal(decorator2):
        import simple
        simple.hello('Guido')

    # Use a module with decorator1 and decorator2 meẗal applied
    with meẗal(decorator1), meẗal(decorator2):
        import simple
        simple.hello('Guido')

In fact, completely different modules can import the same module, each
with different meẗal applied to it.  Try doing that with normal
decorators!

How it Works
============
When activated, Meẗal monitors all import statements in your program
and looks for identifiers that include an metal umlaut (such names are
said to be "meẗalized").  If found, those definitions are firstly
replaced by non-umlaut names.  Thus, if your program looks like this:

    # simple.py
    def ḧellö(name):
        print('Hello', name)

You don't use the umlauts when calling.  You simply write code like
you always did before.  For example:

    import simple
    simple.hello('Guido')

This behavior allows Meẗal to be added to existing programs without
changing any other code--simply put in umlauts in the names of the
functions that support meẗalization and they'll be wrapped seamlessly.

If you put the import statements inside a with-statement you can
have a decorator automatically applied to the meẗalized definitions
for that import. For example,

    import meẗal
    with meẗal(decorator):
        import simple

is equivalent to doing the following:

    # simple.py

    @decorator
    def hello(name):
        print('Hello', name)

However, unlike a normal decorator, keep in mind that this wrapping
only applies in the file that actually performed the meẗalized import.
If other files have imported simple, they won't see the extra meẗal
that's been applied.  Too bad for them--although they could be applying
their own meẗal.

If the decorator takes arguments, simply supply them.  For example,

    import meẗal
    with meẗal(decorator, arg1, arg2):
        import simple

is equivalent to doing this:

    # simple.py

    @decorator(arg1, arg2)
    def hello(name):
        print('Hello', name)

You might be asking how Meẗal is able to apply different decorators
to different import statements and keep the resulting functions
separate?  That question is easily answered by reading the source.

Meẗal - Better than Explicit
============================
Meẗal allows framework builders to explicitly indicate those functions
that could be assisted with the addition of some meẗal.  However,
unlike a normal decorator, it puts the power back into the hands of
the end-user where it belongs.  In this arrangement, everyone wins.
For example, if code is running slow, framework authors can simply
tell users to try putting a bit of meẗal on it. Users then get the
full say on what meẗal they apply.  What's more, different users can
easily apply the meẗal of their choice without worrying about
others--no need for bikesheds here! Yes, the benefits are quite clear.

Compatibility
=============
Meẗal only works with Python 3.  If you love Python and you're still
coding in Python 2, well, then fuck you.

Limitations of Meẗal
====================
None are known or anticipated.

Author
======
Meẗal is the creation of David Beazley (@dabeaz) who disavows all involvement.
'''

import sys
import builtins
import types
from contextlib import contextmanager
from unicodedata import normalize

__meẗalized__ = []
_meẗalizers = []

def _meẗalizing_import(*args, _builtin_import = __import__, **kwargs):
    module = _builtin_import(*args, **kwargs)
    if not hasattr(module, '__meẗalized__'):
        names = dir(module)
        normed_names = [normalize('NFD', name) for name in names]
        meẗalized_names = [(name, normed.replace('\u0308',''))
                            for name, normed in zip(names, normed_names) if '\u0308' in normed]
        setattr(module, '__meẗalized__', [normed for _,normed in meẗalized_names])
        for name, normed in meẗalized_names:
            setattr(module, normed, module.__dict__.pop(name))

    if not _meẗalizers:
        return module

    meẗalized = types.ModuleType(module.__name__)
    meẗalized.__dict__.update(module.__dict__)
    for name in module.__meẗalized__:
        defn = getattr(meẗalized, name)
        for decorate, dargs, dkwargs in reversed(_meẗalizers):
            if dargs or dkwargs:
                defn = decorate(*dargs,**dkwargs)(defn)
            else:
                defn = decorate(defn)
        setattr(meẗalized, name, defn)
    return meẗalized

builtins.__import__ = _meẗalizing_import

@contextmanager
def meẗalmanager(decorate, dargs, dkwargs):
    _meẗalizers.append((decorate, dargs, dkwargs))
    try:
        yield
    finally:
        _meẗalizers.pop()

class Meẗal(types.ModuleType):
    __ = sys.modules[__name__]
    def __call__(self, decorator, *args, **kwargs):
        return meẗalmanager(decorator, args, kwargs)

sys.modules[__name__] = Meẗal(__name__)

