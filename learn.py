import numpy as np 
import multiprocessing as multp
from multiprocessing import Pool as Pool
import time
# global variables
N = 80000
MAXCPUS = 8
STRIDE  = 3
CPUS = np.array([4,8])

def pf(s):
    """@todo: Docstring for pf

    :s: @todo
    :returns: @todo

    """
    #print('hello %s'%s) 
    val= 0
    n  = 5000
    #print('%d iter %d' %(s,i))
    x = np.arange(n)
    xsq = np.sqrt(x)
    val = (val+sum(xsq))/n
    #print ('%d has val:%f'%(s, val))
    return (s,val)

def main(arg1):
    """Run the map a few times and see the speedup

    :arg1: @todo
    :returns: @todo

    """
    times = np.zeros(CPUS.shape)
    for i, CPUC in enumerate(CPUS):
        pool = Pool(CPUC+1)
        ts = time.time()
        result = pool.map_async(pf, np.arange(N), 
                chunksize=N/num_chunks)
        pool.close()
        pool.join()
        te = time.time()-ts
        times[i] = te
        print("success: %s" % result.successful())
        #print("AsyncResult: ", result.get())
    print(times)
    scala = np.log(times * (CPUS))
    print(scala)
    speedup = times[0]/times[-1]
    print("speedup from %d to %d cores: %f"%
            (CPUS[0], CPUS[-1], speedup))
    print("chunksize must be tuned for optimal 
           performance, it is not enough to go big") 
