""" The decorators module contains decorators to make parallelizing code easier
Right now they do not work because of un picklability of function objects
"""
def unpack_decoration(func):
    """Takes a function that expects many args and wraps it 
    to take a single tuple. This allows it to be used in a pool.map function call.

    :func: the function to wrap
    :returns: the wrapper

    """
    @wraps
    def tuple_func(tupl):
        return func(*tupl)
    return tuple_func

@unpack_decoration
def par_add(a,b):
    return op.add(a,b)
