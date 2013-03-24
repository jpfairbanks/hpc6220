from functools import wraps
import operator as op
import math
import numpy as np
import sys
import multiprocessing
from multiprocessing import Process
sys.path.append('test_harness')
from timedict import timedict

# Without using numpy
def star_add(opperands):
    """Wrap operation.add so that it takes a tuple.

    :opperands: tuple of things to add
    :returns: the sum

    """
    return op.add(*opperands)


def reduc_tree(pool, oper, seq, NP):
    """A reduction tree implementation using pool as the parallel workers
    for an arbitrary binary operator.
    :oper: takes a point (a,b) and returns a single item.
    :seq: The sequence to reduce, it will not be copied
    :NP: The number of processing elements
    :returns: The sum of seq.

    """
    tmp_seq = seq
    while len(tmp_seq) > 1:
        n = len(tmp_seq)
        evens = tmp_seq[0::2]
        odds  = tmp_seq[1::2]
        end   = tmp_seq[-1]
        argseq = zip(evens, odds)
        tmp_seq = pool.map(oper, argseq)
        if n%2 == 1:
            oper((tmp_seq[0], end))
    return tmp_seq

def MP_main(pool, num_procs):
    """Using multiproccessing to see if it is faster
    :returns: The sum over SEQ

    """
    answers = SEQ
    count = reduc_tree(pool, star_add, answers, NP)
    return count


# With NUMPY much faster
def np_norm(arr):
    return np.sqrt(arr*arr)
    
def partition(seq, NP):
    """Partition the sequence for the processors

    :seq: any array like 
    :returns: an array-like of array-likes

    """
    n = len(seq)
    elts_per_p = n/(NP)
    #print(elts_per_p)
    indices = [(int(i*elts_per_p), int((i+1)*elts_per_p)) 
                    for i in range(NP)]
    arrays  = [seq[mini:maxi] for mini, maxi in indices]
    return arrays

def packed_reduction(pool, seq, NP):
    """A reduction tree implementation using pool as the parallel workers
    for an arbitrary binary operator.
    assuming that the data has been partitioned into seq sequences

    :oper: takes a point (a,b) and returns a single item.
    :seq: The sequence to reduce, it will not be copied
    :NP: The number of processing elements
    :returns: The sum of seq.

    """
    #TODO add operator field
    parts = pool.map(np.sum, seq)
    total_sum = np.sum(parts)
    return total_sum


def dot(tupl):
    return np.dot(*tupl)

def par_matvec(pool, args, np):
    timer.tic('map')
    partials = pool.map(dot, args)
    timer.toc('map')
    return partials

def numpy_main(pool, num_procs):
    """Using multiproccessing to see if it is faster
    :returns: The sum over SEQ

    """
    #arrays = partition(SEQ, NP)
    #answers = pool.map(np_norm, arrays)
    #print(answers)
    timer.tic('partition')
    block_rows = partition(MAT, num_procs)
    timer.toc('partition')
    vec_copies = num_procs*[SEQ]
    timer.tic('zip')
    args = zip(block_rows, vec_copies)
    timer.toc('zip')
    answers = par_matvec(pool, args, num_procs)
    print([a.shape for a in answers])
    #answers = np.concatenate(answers, axis=0)
    answers = packed_reduction(pool, answers, num_procs)
    return answers

def serial_main():
    """Does the main without any parallel overhead
    :returns: the sum of the matvec

    """
    #answers = np.sqrt((SEQ * SEQ))
    answers = MAT.dot(SEQ)
    count = np.sum(answers)
    return count

if __name__ == '__main__':
    timer = timedict()
    scale = 14
    SEQ = np.random.random(2**scale)
    MAT = np.random.rand(2**scale, 2**scale)
    #print(MAT)
    print(SEQ)
    MAX_PROCS = 4
    NP = 4
    pool = multiprocessing.Pool(processes=NP)
    par_name = 'MP'+str(MAX_PROCS)
    npname = 'NumPy'+str(MAX_PROCS)
    timer.tic(0)
    count = serial_main()
    timer.toc(0)
    print('serial')

    print('we cannot do matvec without numpy')
    timer.tic(par_name)
    mp_count = MP_main(pool, NP)
    timer.toc(par_name)
    print('mp')

    timer.tic(npname)
    np_count = numpy_main(pool, NP)
    timer.toc(npname)
    print('np')

    print('num_primes:%s,%s,%s' % (count, mp_count, np_count))
    print(repr(timer.ends))
    print('Multiprocs speedup: %f' %
	    (timer.ends[0]/timer.ends[par_name]))
    print('NumPy speedup: %f' %
	    (timer.ends[0]/timer.ends[npname]))
