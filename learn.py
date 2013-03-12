import numpy as np 
import multiprocessing as multp
from multiprocessing import Pool as Pool
import time
MAXCPUS = 8
def pf(s):
    """@todo: Docstring for pf

    :s: @todo
    :returns: @todo

    """
    #print('hello %s'%s) 
    val=0
    for i in range(5):
        #print('%d iter %d' %(s,i))
        x = np.arange(1000)
        xsq = np.sqrt(x)
        val = (val+sum(xsq))/2
        #print ('%d has val:%f'%(s, val))
    return (s,val)
times = np.zeros(MAXCPUS/2)
for CPUS in range(0,MAXCPUS,2):
    pool = Pool(CPUS+1)
    ts = time.time()
    result = pool.map_async(pf, np.arange(8000), chunksize=10)
    pool.close()
    pool.join()
    te = time.time()-ts
    times[(CPUS)/2] = te
    print("success: %s" % result.successful())
    #print("AsyncResult: ", result.get())
print(times)
scala = np.log(times * (np.arange(MAXCPUS/2)+1))
print(scala)
speedup = times[0]/times[-1]
print("speedup on %d cores: %f"%(MAXCPUS, speedup))
print("chunksize must be tuned for optimal performance, it is not enough to go big") 
