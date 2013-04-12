import par_args
import parutils
import numpy.random as random
import sys
import multiprocessing
from multiprocessing import Process
sys.path.append('test_harness')
from timedict import timedict


# The mains to compare, partitions, divide and conquor, serial
def flat_main(pool, SEQ, num_procs):
    """Using multiproccessing to see if it is faster
    :returns: The sum over SEQ

    """
    arrays  = parutils.partition(SEQ, num_procs)
    count   = parutils.packed_reduction(pool, sum, arrays, num_procs)
    return count

def tree_main(pool, SEQ, num_procs):
    """Using multiproccessing to see if it is faster
    Try using the recursive tree approach to the reduction.
    :returns: The sum over SEQ

    """
    answers = SEQ
    count = parutils.reduction_tree(pool, parutils.star_add, answers, NP)
    return count

def serial_main(SEQ):
    """Does the main without any parallel overhead
    :returns: the sum over the array

    """
    count = sum(SEQ)
    return count

def big_main(args):
    # Setup
    timer = timedict()
    scale = args.scale
    NP = args.procs
    par_name = 'Tree'+str(NP)
    flat_name = 'Flat'+str(NP)
    timer.tic('spawning pool')
    pool = multiprocessing.Pool(processes=NP)
    timer.toc('spawning pool')
    SEQ = random.random(2**scale)
    print(SEQ)


    # Testing

    timer.tic(0)
    count = serial_main(SEQ)
    timer.toc(0)
    print('serial')

    if args.tree:
        timer.tic(par_name)
        tree_count = tree_main(pool, SEQ, NP)[0]
        timer.toc(par_name)
        print('tree')

    timer.tic(flat_name)
    np_count = flat_main(pool, SEQ, NP)
    timer.toc(flat_name)
    print('flat')

    # Reporting
    print('sum:%s,%s' % (count, np_count))

    eps = .00001
    assert count-np_count<eps, "we got the wrong answer"
    if args.tree:
        print('sum:%s,%s' % (count, tree_count))
        assert count == tree_count
    
    print(repr(timer.ends))
    if args.tree:
        print('Tree speedup: %f' %
                (timer.ends[0]/timer.ends[par_name]))
    print('Flat speedup: %f' %
	    (timer.ends[0]/timer.ends[flat_name]))
    return (scale, NP, timer[0], timer[flat_name])

if __name__ == '__main__':

    args = par_args.get_args()
    ans = big_main(args)
    print(ans)
