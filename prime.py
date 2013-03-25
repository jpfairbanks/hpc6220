import par_args
import parutils
from functools import wraps
import operator as op
import math
import numpy as np
import numpy.random as random
import sys
import multiprocessing
from multiprocessing import Process
sys.path.append('test_harness')
from timedict import timedict

# Useless tasks to generate operations
def is_prime(n):
    if n % 2 == 0:
        return 0

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return 0
    return 1


# The mains to compare, partitions, divide and conquor, serial
def flat_main(pool, num_procs):
    """Using multiproccessing to see if it is faster
    :returns: The sum over SEQ

    """
    timer.tic("map_flat")
    bools = pool.map(is_prime, SEQ, scale)
    timer.toc("map_flat")
    timer.tic("list_flat")
    answers = list(bools)
    timer.toc("list_flat")
    timer.tic("partition")
    arrays  = parutils.partition(answers, num_procs)
    timer.toc("partition")
    timer.tic("reduce_flat")
    count   = parutils.packed_reduction(pool, sum, arrays, num_procs)
    timer.toc("reduce_flat")
    return count

def tree_main(pool, num_procs):
    """Using multiproccessing to see if it is faster
    Try using the recursive tree approach to the reduction.
    :returns: The sum over SEQ

    """
    timer.tic("map_tree")
    bools = pool.map(is_prime, SEQ, scale)
    timer.toc("map_tree")
    timer.tic("list_tree")
    answers = list(bools)
    timer.toc("list_tree")
    timer.tic("reduce_tree")
    count = parutils.reduction_tree(pool, parutils.star_add, answers, NP)
    timer.toc("reduce_tree")
    return count

def serial_main():
    """Does the main without any parallel overhead
    :returns: the sum over the array

    """
    answers = map(is_prime, SEQ)
    count = sum(answers)
    return count

if __name__ == '__main__':
    # Setup

    timer = timedict()
    args = par_args.get_args()
    scale = args.scale
    NP = args.procs
    par_name = 'Tree'+str(NP)
    flat_name = 'Flat'+str(NP)
    timer.tic('spawning pool')
    pool = multiprocessing.Pool(processes=NP)
    timer.toc('spawning pool')
    SEQ = random.random_integers(100000,1000000, size=2**scale)
    print(SEQ)


    # Testing

    timer.tic(0)
    count = serial_main()
    timer.toc(0)
    print('serial')

    timer.tic(par_name)
    tree_count = -1
    if args.tree:
        tree_count = tree_main(pool, NP)[0]
    timer.toc(par_name)
    print('tree')

    timer.tic(flat_name)
    np_count = flat_main(pool, NP)
    timer.toc(flat_name)
    print('flat')

    # Reporting

    print('sum:%s,%s,%s' % (count, tree_count, np_count))
    print(repr(timer.ends))
    print('Tree speedup: %f' %
	    (timer.ends[0]/timer.ends[par_name]))
    print('Flat speedup: %f' %
	    (timer.ends[0]/timer.ends[flat_name]))
