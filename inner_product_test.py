from __future__ import print_function
import par_args
import parutils
import numpy.random as random
import numpy as np
import sys
import multiprocessing
from multiprocessing import Process
sys.path.append('test_harness')
from timedict import timedict
from testio import *


# The mains to compare, partitions, divide and conquor, serial
def flat_main(pool, SEQ, mask, num_procs):
    """Using multiproccessing to see if it is faster
    :returns: The sum over SEQ

    """
    arrays  = parutils.partition(SEQ, num_procs)
    masks   = parutils.partition(mask, num_procs)
    result  = parutils.inner_product(pool, arrays, masks, num_procs)
    return result


def serial_main(SEQ, mask):
    """Does the main without any parallel overhead
    :returns: the sum over the array

    """
    result = parutils.serial_inner_product((SEQ, mask))
    return result
def big_main(args):
    """Does the setup and teardown to test both methods
    
    """
    # Setup
    timer = timedict()
    NP = args.procs
    scale = args.scale
    if args.verbose:
        if args.tree:
            print('no tree method for inner_product because they are too slow')
    flat_name = 'Flat'+str(NP)
    timer.tic('spawning pool')
    pool = multiprocessing.Pool(processes=NP)
    timer.toc('spawning pool')
    SEQ = np.arange(0,2**scale)
    mask = random.random_integers(0,1,2**scale)
    if args.verbose:
        vprint("SEQ",  SEQ)
        vprint("mask", mask)
 

    # Testing

    timer.tic(0)
    arr = serial_main(SEQ, mask)
    timer.toc(0)
    if args.verbose:
        print('serial done')

    timer.tic(flat_name)
    par_arr = flat_main(pool,SEQ, mask, NP)
    timer.toc(flat_name)
    #print('flat')

    # Reporting

    assert (SEQ*mask).sum() == arr, "we did not get the right answer"
    #print('Same result: %s' % (par_arr == arr))
    #print(repr(timer.ends))
    flat_speedup = timer.ends[0]/timer.ends[flat_name]
    #print('Flat speedup: %f' %
    #	    (flat_speedup))
    pool.close()
    pool.join()
    ans = (scale, NP, timer[0], timer[flat_name])
    return ans

if __name__ == '__main__':
    args = par_args.get_args()
    scale = args.scale
    NP = args.procs
    ans = big_main(args)
    print("{0},{1},{2},{3}".format(*ans))
