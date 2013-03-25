# Publishable 
## Dense Matrix Vector Multiplication
The clear winner is serial numpy. There is just no way to be optimized C BLAS
for dense numerical linear algebra.

## For native python

### Map
What is the overhead of the dynamic scheduler?
How does chunk size affect the performance
I seem to have found that log(N) provides a good chunk size.
### Reduction 
Should you do the log(P) depth solution where each processor adds the adjacent elements of the array together until only one element remains?
Or should the work be cut up into the largest possible serial chunks to be processed sequentially.
The flat approach with each of the $p$ processors conquering $n/p$ of the work
performs better as the size of the partitions increases. This means that 
for a fixed $p$ more work elements means better speedup. I believe this has to do
with the overhead associated with forking OS level processes and function call 
overhead.

# Notes

Compare the performance of a multiprocessing.Array and multiprocessing.RawArray
Arrays have a lock that makes writes atomic.

Concurrent Futures allow for a higher level api but create unexpected bahavior.

## Map Reduce

Use this to count words in some big document collection.
http://docs.python.org/2/library/collections.html#collections.Counter
http://www.dalkescientific.com/writings/diary/archive/2012/01/19/concurrent.futures.html
