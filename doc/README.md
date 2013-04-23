# Parallel Primitives in Python

Making parallel programming accesible to most programmers is essential to improve scalability
of our computing systems into the future. This access is primarily blocked by the steep learning 
curve and poor quality of the HPC development environment. In order to improve this, I am looking 
at implementing some parallel primatives in Python using multiprocessing for shared memory. 

I will be investigating these algorithms.

    - Simple parallel map
    - Array Reduction using Trees
    - Array Scans
    - Pack
    - Inner Product
    - Matrix Vector Product
    - Sparse MatVec
    - PageRank for CSR Graph

I think that making these algorithms accessibles as function calls to the python programmers 
will enable them to take advantage of multicore architectures without having to develop in a 
low level language. 

# Programming Models

## Map-Reduce

Many things can be accelerated by using data parallelism. 
In this programming model the programmer will be allowed to use map and reduce to create parallel work. 
The map phases correspond to parallel for loops where there are no data dependence between iterations.
The reduce phases are data dependent but must be reductions of a binary associative operator.
There will be a master serial controller that dispatches these parallel tasks. 
If the programmer is restricted to using Map and Reduce operations on their data, 
then they are prevented from creating any deadlocks. They could create an iterative algorithm that does
not converge but they cannot create a situation where processes are waiting because of dependence. 
As any dependent data will be computed at the conclusion of the previous map or reduce phase.
We will avoid a common problem with Hadoop that forces a reduce phase after every map phase. 
The serial controller logic will not be restricted.

## Vector operations

The array scans are important shared memory operations for expressing parallelism.


## Bulk Synchronous Parallel

We can compute sparse matrix operations in parallel using BSP model. This is the gateway to 
programming distributed systems. The benefit of programming for shared memory is that good 
performance will be easier to obtain and show that speed up is possible. 

"BSP algorithms are only interesting where there is some irregularity in the computation" 
--David Ediger.

# Expected Timeline
Date        Task       
-----       ------------
03-20       Proposal Done
03-31       Implementations of Map and Tree Reduction
04-05       Implementation of Scans
04-14       Implementation of CSR MatVec
04-20       Begin Writing

# Risks

Well I could provide tools that do not provide significant speedup. Hopefully this would be due to limitations in the Python interpreter and will improve as the interpreter improves.
Another risk is that of not finishing all of the goals that I have outlined. Going from map-reduce parallelism up to BSP is a large range. Perhaps I should just focus on getting up to the array scans.
# References
http://ipython.org/ipython-doc/dev/parallel/parallel_intro.html
http://ipython.org/ipython-doc/dev/parallel/parallel_demos.html#parallel-examples
https://www.cs.cmu.edu/~blelloch/papers/Ble90.pdf

# LICENSE

Copyright (c) 2013, James P. Fairbanks
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of the Georgia Institute of Technology nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
