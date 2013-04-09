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


# The mains to compare, partitions, divide and conquor, serial
def flat_main(pool, SEQ, mask, num_procs):
    """Using multiproccessing to see if it is faster
    :returns: The sum over SEQ

    """
    arrays  = parutils.partition(SEQ, num_procs)
    masks   = parutils.partition(mask, num_procs)
    result  = parutils.pack(pool, arrays, masks, num_procs)
    return result


def serial_main(SEQ, mask):
    """Does the main without any parallel overhead
    :returns: the sum over the array

    """
    result = parutils.serial_pack((SEQ, mask))
    return result
def big_main():
    """Does the setup and teardown to test both methods
    
    """
    # Setup
    timer = timedict()
    scale = args.scale
    NP = args.procs
    if args.verbose:
        if args.tree:
            print('no tree method for scans because they are too slow')
    flat_name = 'Flat'+str(NP)
    timer.tic('spawning pool')
    pool = multiprocessing.Pool(processes=NP)
    timer.toc('spawning pool')
    SEQ = np.arange(0,2**scale)
    mask = random.random_integers(0,1,2**scale)
    if args.verbose:
        print(SEQ)


    # Testing

    timer.tic(0)
    arr = serial_main(SEQ, mask)
    timer.toc(0)
    print('serial')

    timer.tic(flat_name)
    seqs = flat_main(pool,SEQ, mask, NP)
    par_arr = parutils.serial_concat(seqs)
    timer.toc(flat_name)
    print('flat')

    # Reporting

    #print('sum:%s,%s,%s' % (count, tree_count, np_count))
    print('Same result: %s' % (par_arr == arr))
    print(repr(timer.ends))
    flat_speedup = timer.ends[0]/timer.ends[flat_name]
    print('Flat speedup: %f' %
	    (flat_speedup))
    return flat_speedup

if __name__ == '__main__':
    args = par_args.get_args()
    big_main()
