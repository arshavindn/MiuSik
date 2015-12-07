import time
from functools import wraps


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" %
               (function.func_name, str(t1-t0))
               )
        return result
    return function_timer


def test_yield():
    for i in range(100000):
        yield i

def test_append():
    lst = []
    for i in range(100000):
        lst.append(i)
    return lst

@fn_timer
def run_test():
    return test_append()

run_test()
# 0.0169999599457 seconds
