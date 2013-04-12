% HPC6220 Project
% James Fairbanks
% 2013-03-26

# Goals
I set out to implement Reduction, Scan, Pack, and Inner Product for shared memory Python.
Since this is a project status update I have played fast and loose with these numbers.
# Results
I have been able to implement all of the methods and run tests to validate their consistency
and their speedup, against the serial version. 

## Reduce and Scan
I implemented two forms of reduce, one based on a PRAM reduction tree
and a more distributed memory style algorithm based on partitioning. 
The reduction tree performs terribly compared to the serial implementation. 

The break even point for the Partitioned approach to a + reduction is 4 cores $2^{15}$ elements.
For the reduction tree at this scale the speedup is 0.031702 over the serial implementation.

At scale 25 $2^{25}$ elements, the speedup for the Partitioned approach is 3.46. I am proud of this result for 4 cores.
This experiment indicated that implementing Scan using any tree like approach was not going to be efficient. 
Thus for scan I also used a partitioning approach. The array is broken into $P$ pieces and each piece is scanned separately in serial. 
The last element of each scan is the offset accumulated over that piece. These offsets are then scanned serially by the master process, 
and the resulting corrections are propagated along the original array. This requires two passes over the data set and thus we should 
expect it to be less scalable. This is reflected in the experimental data. The parallel scan on 4 cores breaks even between scale 18 and 19. And for 
scale 25 the speedup is 1.6. My hypothesis for this performance hit is that the second pass over the data hurts as well as the serial scan of size $P$
leaves all but one processor idle during the middle phase.

## Pack

Pack required a bit more work because it takes two arrays and returns a third with a different length.
Both the mask and the data array are partitioned identically.
Again the partitioned approach was used. This mask is first scanned to find the indexes of the final element positions. 
Then one pass is made over the data array. During this pass we check the mask to see if we should copy this element and 
if yes, it goes into the destination position given by scan(mask). One data dependent issue with this implementation, 
is that some processors could make many more copies than other processors. This could produce load balance issues if the time
to do the copy is large relative to the cost of the check. 

Pack breaks even at scale 14 and 4 threads. The speedup on 4 cores and scale 25 is 2.98.

## Inner Product 

The inner product was easy to implement and breaks even at scale 14. The speedup at scale 25 with 4 cores is 2.83.

# Discussion

This has been an enjoyable project so far. I am happy to see speedup is possible in a higher level language.
