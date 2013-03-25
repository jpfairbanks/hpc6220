import par_args
import parutils
import numpy.random as random
import sys
import multiprocessing
from multiprocessing import Process
sys.path.append('test_harness')
from timedict import timedict


# The mains to compare, partitions, divide and conquor, serial
def flat_main(pool, num_procs):
    """Using multiproccessing to see if it is faster
    :returns: The sum over SEQ

    """
    arrays  = parutils.partition(SEQ, num_procs)
    count   = parutils.packed_scan(pool, parutils.serial_scan, arrays, num_procs)
    initial = count[0]
    for s in count[1:]:
        initial.extend(s)
    return initial


def serial_main():
    """Does the main without any parallel overhead
    :returns: the sum over the array

    """
    count = parutils.serial_scan(SEQ)
    return count

if __name__ == '__main__':
    # Setup
    timer = timedict()
    args = par_args.get_args()
    scale = args.scale
    NP = args.procs
    if args.verbose:
        if args.tree:
            print('no tree method for scans because they are too slow')
    flat_name = 'Flat'+str(NP)
    timer.tic('spawning pool')
    pool = multiprocessing.Pool(processes=NP)
    timer.toc('spawning pool')
    SEQ = random.random_integers(0,1,2**scale)
    if args.verbose:
        print(SEQ)


    # Testing

    timer.tic(0)
    count = serial_main()
    timer.toc(0)
    print('serial')

    timer.tic(flat_name)
    np_count = flat_main(pool, NP)
    timer.toc(flat_name)
    print('flat')

    # Reporting

    #print('sum:%s,%s,%s' % (count, tree_count, np_count))
    print('Same result: %s' % (np_count == count))
    print(repr(timer.ends))
    print('Flat speedup: %f' %
	    (timer.ends[0]/timer.ends[flat_name]))
