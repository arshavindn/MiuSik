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

lst1 = range(100000)

lst2 = [2, 50, 17, 8, 33, 12]

def test_filter():
    print filter(lambda x: x in lst2, lst1)

def test_for():
    result = []
    for x in lst1:
        if x in lst2:
            result.append(x)
    print result


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
    return test_filter()

run_test()
# 0.0480000972748 seconds
