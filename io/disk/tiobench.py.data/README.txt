This program runs  a multi-threaded I/O benchmark test to measure file system performance in four basic operations: 
sequential read, random read, sequential write, and random write based on the inputs specified in the multiplexer file.

 Inputs needed in yaml file:
----------------------------

target: The directory in which to test. Defaults to ., the current directory.
blocks: The blocksize in Bytes to use. Defaults to 4096.
threads: The number of concurrent test threads.
size: The total size in MBytes of the files may use together.
numruns: This number specifies over how many runs each test should be averaged.
iteration: Number of iterations the test needs to be run.

