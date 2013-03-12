# Parallel Primitives in Python

Making parallel programming accesible to most programmers is essential to improve scalability
of our computing systems into the future. This access is primarily blocked by the steep learning 
curve and poor quality of the HPC development environment. In order to improve this, I am looking 
at implementing some parallel primatives in Python using multiprocessing for shared memory. 

I will be investigating these algorithms.

    - Array Reduction using Trees
    - Array Scans
    - Inner Product
    - Matrix Vector Product
    - Sparse MatVec
    - PageRank for CSR Graph
    

I think that making these algorithms accessibles as function calls to the python programmers 
will enable them to take advantage of multicore architectures without having to develop in a 
low level language. 

# Programming Models

## Vector operations

The array scans are important shared memory operations for expressing parallelism.

## Bulk Synchronous Parallel

We can compute sparse matrix operations in parallel using BSP model. This is the gateway to 
programming distributed systems. The benefit of programming for shared memory is that good 
performance will be easier to obtain and show that speed up is possible. 

"BSP algorithms are only interesting where there is some irregularity in the computation" 
--David Ediger.

