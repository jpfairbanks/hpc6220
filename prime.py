import concurrent.futures
import math
import numpy as np
import sys
import multiprocessing
from multiprocessing import Process
sys.path.append('test_harness')
from timedict import timedict

timer = timedict()
PRIMES = np.random.randint(1000000000, size=8000)

def is_prime(n):
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def conc_main(num_procs):
    with concurrent.futures.ProcessPoolExecutor(num_procs) as executor:
        print(executor)
        bools = executor.map(is_prime, PRIMES)
    print(bools)
    return bools

def MP_main(num_procs):
    """Using multiproccessing to see if it is faster
    :returns: @todo

    """
    bools = None
    pool = multiprocessing.Pool(processes=num_procs)
    bools = pool.map(is_prime, PRIMES)
    return bools

def serial_main():
    """Does the main without any parallel overhead
    :returns: nothing because it prints

    """
    bools = map(is_prime, PRIMES)
    return bools

if __name__ == '__main__':
    MAX_PROCS = 4
    timer.tic(0)
    serial_bools = list(serial_main())
    timer.toc(0)
    print('serial')

    timer.tic('MP'+str(MAX_PROCS))
    mp_bools = list(MP_main(MAX_PROCS))
    timer.toc('MP'+str(MAX_PROCS))
    print('mp')

    timer.tic(MAX_PROCS)
    print('concurrent')
    #conc_bools = conc_main(MAX_PROCS)
    #dones = concurrent.futures.wait(conc_bools)
    timer.toc(MAX_PROCS)

    print('equal %d' % (serial_bools == mp_bools))
    #print('equal %d' % (conc_bools == mp_bools))
    print(repr(timer.ends))
    print('Concurrent speedup: %f' %
	    (timer.ends[0]/timer.ends[MAX_PROCS]))
    print('Multiprocs speedup: %f' %
	    (timer.ends[0]/timer.ends['MP'+str(MAX_PROCS)]))
