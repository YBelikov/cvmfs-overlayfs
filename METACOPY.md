<h1>This file contains a report about performance changes in various metadata modifying operations for Linux OverlayFS with "metacopy" mounting parameter set to "on".</h1>

<h2>Benchmarking setup:</h2>
To measure and compare impact made by this feature I decided to focus my investigation on the average execution time of syscalls affecting files' metadata. 
In particular we were interested in two most frequently performed operations on typical CVMFS repository: chmod and chown. 
Alma Linux 9 was selected as the main testing and development OS on physical device as Alma distribution is a principal one in CERN.

The benchmarking for chmod operation was performed under the following conditions:
1. Three directories were created in local filesystem: one that does not belong to overlay FS, one directory used as a lower (readonly) layer in overlay FS without any additional configuration parameters, and one lower layer directory for overlay FS with metacopy only feature.
2. create_dir.py script seeded 100 random files in the base dir with sizes in the interval 100 to 300MB that were copied with a corresponding utility script to both lower layer directories.
3. Both overlay FS were mounted. 
4. perform_benchmark.py script launched 1000 operations per each file in a directory giving us 100 000 chmod calls.
5. The time of each call was measured with time.per_counter().
6. Benchmarking script gathered information about average time that call took to finish and saved these results as pairs (file size, average execution time) to specified output directories in the text format.
7. plot_comparison.py was used to plot the comparison chart.
