from functools import partial, reduce

def pipe(val, *funcs):
    for func in funcs:
        val = func(val)
    return val

compose_two = lambda f, g: lambda *args, **kwargs: f(g(*args, **kwargs))

compose = lambda *funcs: reduce(compose_two, reversed(funcs))

class Apply:
    pass

def count_apply(*args):
    pass


def thread_first(val, *forms):
    def fun(val, form):
        if callable(form):
            return form(val)
        func, *args = form
        return func(val, *args)
    return reduce(fun, forms, val)

def inc(x, i = 1):
    return x + i

def mul(x, m = 2):
    return x * m

composed = compose(inc, mul, mul)

print(composed(2))

print(thread_first(2,
                    (inc, 2),
                    (mul, 1)))
print(Apply is Apply)
print(callable(Apply))

