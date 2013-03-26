% HPC6220 Project
% James Fairbanks
% 2013-03-26

# Parallel Primitives in Python

Making parallel programming accessible to most programmers is essential to scaling our
computing systems into the future. This access is primarily blocked by the steep learning 
curve and quality of the HPC development environment. In order to improve this, I am looking 
at implementing some parallel primitives in Python using multiprocessing for shared memory. 

I will be investigating these algorithms.

    - Parallel map
    - Array Reduction using Trees
    - Array Reduction using partitioning
    - Array Scan
    - Pack
    - Inner Product

I think that making these algorithms accessible as function calls to the Python programmers 
will enable them to take advantage of multicore architectures without having to develop in a 
low level language. 


# Map-Reduce

Many things can be accelerated by using data parallelism. 
In this programming model the programmer will be allowed to use map and reduce to create parallel work. 
The map phases correspond to parallel for-loops where there is no data dependence between iterations.
The reduce phases have data dependence but must be reductions of a binary associative operator.
There is a master process that dispatches these parallel tasks. 
If the programmer is restricted to using Map and Reduce operations on their data, 
then they are prevented from creating any deadlocks. 

# Vector operations

Array scans are important shared memory operations for expressing parallelism.
According to Blelloch, parallel map and array scans are sufficient for PRAM programming.

# Expected Timeline
Date        Task
-----       ------------
03-26       Proposal Done
03-31       Implementations of Map and Tree Reduction
04-05       Implementation of Scan, Pack, Inner Product
04-15       Experimentation        
04-20       Writing

# Risks

I could provide tools that do not provide significant speedup. Hopefully this would be due to limitations 
in the Python interpreter and will improve as the interpreter improves.

# References

 - http://ipython.org/ipython-doc/dev/parallel/parallel_intro.html
 - http://ipython.org/ipython-doc/dev/parallel/parallel_demos.html#parallel-examples
 - https://www.cs.cmu.edu/~blelloch/papers/Ble90.pdf

