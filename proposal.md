# Parallel Primitives in Python

Making parallel programming accessible to most programmers is essential to improve scalability
of our computing systems into the future. This access is primarily blocked by the steep learning 
curve and poor quality of the HPC development environment. In order to improve this, I am looking 
at implementing some parallel primitives in Python using multiprocessing for shared memory. 

I will be investigating these algorithms.

    - Parallel map
    - Array Reduction using Trees
    - Array Reduction using partitioning
    - Array Scans
    - Pack
    - Inner Product

I think that making these algorithms accessible as function calls to the Python programmers 
will enable them to take advantage of multicore architectures without having to develop in a 
low level language. 

# Programming Models

## Map-Reduce

Many things can be accelerated by using data parallelism. 
In this programming model the programmer will be allowed to use map and reduce to create parallel work. 
The map phases correspond to parallel for loops where there are no data dependence between iterations.
The reduce phases have data dependence but must be reductions of a binary associative operator.
There will be a master serial controller that dispatches these parallel tasks. 
If the programmer is restricted to using Map and Reduce operations on their data, 
then they are prevented from creating any deadlocks. 

## Vector operations

The array scans are important shared memory operations for expressing parallelism.
According to Blelloch, parallel map and array scans are sufficient for PRAM programming.


# Expected Timeline
Date        Task
-----       ------------
03-26       Proposal Done
03-31       Implementations of Map and Tree Reduction
04-05       Implementation of Scans
04-14       Experimentation
04-20       Writing

# Risks

Well I could provide tools that do not provide significant speedup. Hopefully this would be due to limitations in the Python interpreter and will improve as the interpreter improves.
Another risk is that of not finishing all of the goals that I have outlined.

# References

- http://ipython.org/ipython-doc/dev/parallel/parallel_intro.html
 - http://ipython.org/ipython-doc/dev/parallel/parallel_demos.html#parallel-examples
 - https://www.cs.cmu.edu/~blelloch/papers/Ble90.pdf

