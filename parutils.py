from __future__ import print_function
import operator as op
import math
import numpy as np
import sys
import multiprocessing
from multiprocessing import Process
sys.path.append('test_harness')
from timedict import timedict
from array import array
vprint = lambda s,o: print('{0}:\n{1}'.format(s,o))
def serial_scan(seq, dtype='d'):
    #print('one iter of serial_scan')
    #print(type(seq))
    #print(seq.dtype)
    #print(seq[0])
    y = array(dtype, seq)
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

def serial_pack(arg):
    """Pack seq into an array if mask[i] = 1
    :arg: a tuple containing the following
        :seq: an array of elements
        :mask: an array of flags 1 means include 0 means ignore
    :returns: the result of the pack as an array

    mask is not checked for bools if there are entries that are not 
    0,1 in the mask the behavior will be bad.

    """
    seq, mask = arg[0], arg[1]
    #vprint('mask', mask.tostring())
    #print(mask)
    indices = serial_scan(mask, dtype='i')
    indices = serial_shift((indices,-1))# dtype='i')
    #vprint('indices', indices)
    num_elts = indices[-1]
    #vprint('num_elts', num_elts)
    y = array('d', range(int(num_elts)+1))
    #vprint('y',y)
    for i in range(0,len(seq),1):
        if mask[i]:
            y[indices[i]] = seq[i]
    return y

def serial_inner_product(arg):
    """Pack seq into an array if mask[i] = 1
    :arg: a tuple containing the following
        :xvec: an array of elements
        :yvec: another array of elements
    :returns: the sum of the elementwise products

    asserts that the len's are the same.

    """
    xvec, yvec = arg[0], arg[1]
    assert(len(xvec) == len(yvec)) , "len(x) != len(y)"
    prods = ( xvec[i] * yvec[i] for i in range(len(xvec)))
    S = sum(prods)
    return S

def serial_concat(seq):
    """reverses the partition function

    :seq: contains a sequence of sequences 
    :returns: @todo

    """
    dtype = seq[0].typecode
    sizes = map(len,seq)
    N = sum(sizes)
    out = array(dtype, seq[0])
    for i in range(1,len(seq)):
        out.extend(seq[i])
    return out
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
    :oper: takes a sequence and returns the scan of it
    :seq: The sequence to reduce, it will not be copied already partitioned by partition()
    :NP: The number of processing elements
    :returns: The sum of seq.

    """
    parts = pool.map(oper, seq)
    addins = oper([0] + [p[-1] for p in parts])
    args = zip(parts, addins)
    prefixes = pool.map(serial_shift, args)
    return prefixes

def pack(pool, seq, mask, num_procs=1):
    """Returns a packed array from applyin mask to seq

    :seq: @todo
    :mask: @todo
    :returns: @todo

    """
    parts = pool.map(serial_pack, zip(seq, mask))
    return parts

def inner_product(pool, xvec, yvec, num_procs=1):
    """Performs the calculation xvec.T * yvec correpsonding to the linear algebra
    standard inner product. also know as the dot product of two vectors.

    :pool: @todo
    :xvec: @todo
    :yvec: @todo
    :num_procs: @todo
    :returns: the final sum 

    """
    parts = pool.map(serial_inner_product, zip(xvec, yvec))
    ans =  sum(parts)
    return ans

if __name__ == '__main__':
    print("this is a library not a main")
