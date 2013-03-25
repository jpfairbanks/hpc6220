import operator as op
import math
import numpy as np
import sys
import multiprocessing
from multiprocessing import Process
sys.path.append('test_harness')
from timedict import timedict
from array import array

def serial_scan(seq, ):
    #print('one iter of serial_scan')
    #print(type(seq))
    #print(seq[0])
    y = array('d', seq)
    for i in range(1,len(seq),1):
        y[i] = y[i-1] + y[i]
    return y

def serial_shift(arg):
    """ inplace operation on seq"""
    seq   = arg[0]
    const = arg[1]
    for i in range(len(seq)):
        seq[i]+=const
    return seq

# You need to do this to a function that expects two arguments
def star_add(opperands):
    """Wrap operation.add so that it takes a tuple.

    :opperands: tuple of things to add
    :returns: the sum

    """
    return op.add(*opperands)


# Use the tree based approach used in class
def reduction_tree(pool, oper, seq, NP):
    """A reduction tree implementation using pool as the parallel workers
    for an arbitrary binary operator. 

    This method has log(NP) depth and does asymptotically optimal work. 
    However performance appears to be awful.

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

# Partition once then map
def partition(seq, NP):
    """Partition the sequence for the processors
    This method can be used to form sequences that can be iterated over.
    With each processor doing a large amount of serial work on each
    element of the sequence.

    Use this with a pool.map(f, partition(seq,NP)) in order to get
    some good speedups.

    f should be a function that take N/NP elements and makes a constant
    number of function calls.

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

def packed_reduction(pool, oper, seq, NP):
    """A reduction tree implementation using pool as the parallel workers
    for an arbitrary reduction operator.

    :pool: a pool of workers.
    :oper: takes a sequence and returns a single item.
    :seq: The sequence to reduce, it will not be copied
    :NP: The number of processing elements
    :returns: The sum of seq.

    """
    parts = pool.map(oper, seq)
    total_sum = oper(parts)
    return total_sum

def packed_scan(pool, oper, seq, NP):
    """A reduction tree implementation using pool as the parallel workers
    for an arbitrary reduction operator.

    :pool: a pool of workers.
    :oper: takes a sequence and returns a single item.
    :seq: The sequence to reduce, it will not be copied
    :NP: The number of processing elements
    :returns: The sum of seq.

    """
    parts = pool.map(oper, seq)
    addins = oper([0] + [p[-1] for p in parts])
    args = zip(parts, addins)
    prefixes = pool.map(serial_shift, args)
    return prefixes

if __name__ == '__main__':
    print("this is a library not a main")
