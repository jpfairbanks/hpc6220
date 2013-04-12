# Process based parallelism using Multiprocessing
In order to expand the accessibility of parallel algorithms
my project creates some basic primitives for parallel algorithms in Python
and analyzes the performance of those primitives.
We will discuss how one can access parallelism in Python and how these constraints 
make certain algorithmic and design choices an imperative for the parallel programmer in Python.

For example Python has a Global Interpreter Lock (GIL) which prevents multiple threads from 
using the interpreter at the same time. This is the result of design decisions that were made in 
1992 when Python threads were first developed [Beazley]. This GIL prevents multicore performance increases
using one python interpreter. Since there is so much code dependent on features that use the GIL 
it was not feasible to remove it. So the Python standard library now contains a module called Multiprocessing
which uses multiple operating system (OS) level processes to run multiple interpreters that can now work in parallel.
Each process has its own GIL which eliminates contention. David Beazley presented a talk at PyCon 2010 that includes 
a thorough study of the contention for the GIL [Beazley].

In order to protect processes from each other, the operating system keep separate memory spaces for each process.
This restricts multiprocessing code in that every object that is shared between processes must go through communication 
channels at the OS level. These communication channels mean that the parallelism that can be used must be a coarser grain 
than in OpenMP shared memory programming or CILK+ programing. We demonstrate this through a comparison of two
algorithms for reducing a numerical operation over an array. The PRAM style algorithm using a reduction tree is 
significantly out performed by both serial reduction and a partitioned reduction that uses one part for each processor. 

## Using the module

The module provide access to multiple process using a similar interface as pthreads.
Because of the overhead of spawning OS processes or pthreads, the library provides a Pool class 
which encapsulates some state about a collection of worker processes. Tasks can be submitted 
manually to the pool. A task corresponds to a function and a tuple of arguments to 
use for the function call. This is considered the manual way to use a pool of workers. 

As a higher level interface to this pool there are several higher order
functions to make using this pool more concise. these functions are all
conceptually a map, but  differ based on their demand for ordered results, and
blocking the calling thread. A map takes a function and a sequence of argument
tuples and evaluates the function on each element of the sequence. 

Most of the code presented here uses pool.map(f, args) which takes a function
and sequence of arguments to that function and returns a sequence of results.
This version blocks the calling thread until all results are available. Another
version of map, pool.map_async(f, args) does not block and returns immediately.
An asynchronous map returns a sequence of objects that contain information
about their state and the value that was returned by evaluating the function
f in parallel. Because asynchronous map does not block, the result objects must
be waited on individually. An exception is raised if a user attempts to
retrieve a result that has not yet been computed. This protects code consuming
these results from using uninitialized values in further computations.
Asynchronous maps are more suited to providing concurrency than parallelism
because the results can be processed as they arrive, however for our purposes
waiting for all results will give better cache performance as we can traverse
arrays in order. 


# For native python

## Map

What is the overhead of the dynamic scheduler?
How does chunk size affect the performance
I seem to have found that log(N) provides a good chunk size.

## Reduction 

Should you do the log(P) depth solution where each processor adds the adjacent
elements of the array together until only one element remains? Or should the
work be cut up into the largest possible serial chunks to be processed
sequentially. The flat approach with each of the $p$ processors conquering
$\frac{n}{p}$ of the work performs better as the size of the partitions increases. This
means that for a fixed $p$ more work elements means better speedup. I believe
this has to do with the overhead associated with forking OS level processes and
function call overhead.

I implemented both a reduction tree and a partitioned algorithm for reduction.
The reduction tree takes the even and odd elements and combines them in pairs.
Each pair 

~~~~
    tmp[i] = evens[i] + odds[i]
~~~~

is a separate task, both logically and
from the perspective of the process pool. This is the PRAM algorithm where we
assume that the number of processors can grow to be as large as possible. 
However in reality the number of processors is physically limited and this approach
pays a large penalty for forming these fine grained tasks.

The partitioning algorithm takes a different approach. Since we know the number of processors,
we can partition the set of inputs contiguously before we start to operate concurrently. 
Each part is given to a single process which can apply the reduction in serial.
These processes return a single value for their entire segment. Since the 
number of processes is small these $p$ values are reduced in serial by the calling process.
This provides a significant speedup over both the serial version and the reduction 
tree versions.


## Scans

I built a function that takes a serial scan and converts it to a parallel scan. 
Because of the poor performance of the divide and conquer approach to reduction,
I chose to implement only the partitioning based scan. The partitioning approach 
is to take the problem and cut it into $p$ pieces that can be operated on independently
in serial. Then we combine these results by propagating an update across each piece.
In this case the serial process is a serial scan, and the updates are created by scanning the
terminal elements of each piece. This produces a two phase algorithm.

As expected the scalability of this scan is approximately a factor of two worse than 
the partitioned reducer. This is expected because there is a second pass over the data in 
order to propagate the updates. This second pass means that the algorithm has a factor of 2 
more work than the serial algorithm which means that scalability is decreased by that same factor of 2.

The partitions are done evenly and are the same in the first and second pass over the data.
There is no attempt to load balance the workers in the process pool, and this will lead to scalability 
problems when the scan operation is something that has a high variance in run time. However for 
arithmetic operations this should not be an issue.

There are implementation differences between the Python2 and Python3 interpreters. One difference that I found to impact performance is the fact that the zip builtin, which takes two sequences and
bindes them together into one sequence of pairs, makes a list in Python2 but a generator in Python3. 
This leads to a slowdown in `SCAN` because the phase where the offsets are computed and passed to 
the phase that propagates the offsets, uses a zip in order to interface with the process pool. This 
is one of the small features of Python that makes writing High Performance Code less straightforward
than in C. In order to crank out the fastest Python code you must be aware about how the builtin 
functions and data structures are implemented.

## Pack
The pack opertion uses the primitive scan in order to identify the final indices of the data in the 
packed output. Since we are using a partitioned approach we do not need the indices to be propagated
this saves the second pass over the data that we make in the general scan. 

## Inner Product
This problem is interesting because we increase the flop to mop ratio. This should be helpful for 
achieving scalability. 
# Dense Matrix Vector Multiplication

The clear winner is serial numpy. There is just no way to beat optimized C BLAS
for dense numerical linear algebra.

# Map Reduce details
One of the benefits of Map Reduce programming is that it is deadlock free.
Because processes do not explicitly wait on other processes they cannot create a cycle of waits that
cannot be resolved.
A Map Reduce programmer can create an iterative algorithm that does
not converge but they cannot create a situation where processes are waiting because of dependence. 
As any dependent data will be computed at the conclusion of the previous map or reduce phase.
We avoid a common problem with Hadoop that forces a reduce phase after every map phase. 
The serial controller logic will not be restricted in any way.

#Bibliography
http://www.dabeaz.com/python/UnderstandingGIL.pdf

# Notes

Compare the performance of a multiprocessing.Array and multiprocessing.RawArray
Arrays have a lock that makes writes atomic.

Concurrent Futures allow for a higher level api but create unexpected behavior.

## Map Reduce

Use this to count words in some big document collection.
http://docs.python.org/2/library/collections.html#collections.Counter
http://www.dalkescientific.com/writings/diary/archive/2012/01/19/concurrent.futures.html
