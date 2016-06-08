Pattern test of the disk, using unique signatures for each block and each iteration of the test.
Designed to check for data corruption issues in the disk and disk controller.

Inputs Needed in yaml file:
---------------------------
disks - Directory (usually mountpoint) to be passed to the test. Directory gets created if not existing.
gigabyte - Disk space that will be used for the test to run.
chunk_mb - Size of the portion of the disk used to run the test. Cannot be larger than the total amount of free RAM.
source - name of the source file located in deps path
make - name of makefile located in deps path
