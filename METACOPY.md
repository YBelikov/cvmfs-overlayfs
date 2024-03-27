<h1>This file contains a report about performance changes in various metadata modifying operations for Linux OverlayFS with "metacopy" mounting parameter set to "on".</h1>

<h2>Benchmarking setup:</h2>
To measure and compare impact made by this feature I decided to focus my investigation on the average execution time of syscalls affecting files' metadata. 
In particular we were interested in two most frequently performed operations on typical CVMFS repository: chmod() and chown(). 
Alma Linux 9 was selected as the main testing and development OS on physical device as Alma distribution is a principal one in CERN.

The benchmarking for chmod() operation was performed under the following conditions:
1. Three directories were created in local filesystem: one that does not belong to overlay FS, one directory used as a lower (readonly) layer in overlay FS without any additional configuration parameters, and one lower layer directory for overlay FS with metacopy only feature.
2. create_dir.py script seeded 400 random files in the base dir with sizes in the interval 100KB to 35MB that were copied with a corresponding utility script to both lower layer directories.
3. Both overlay FS were mounted. 
4. perform_benchmark.py script launched 1000 operations per each file in a directory giving us 400 000 chmod() calls.
5. The time of each call was measured with time.per_counter().
6. Benchmarking script gathered information about average time that call took to finish and saved these results as tuples (file size, average execution time) to specified output directories in the text format.
7. plot_comparison.py was used to plot the comparison chart.

<h2>Operating Systems used in the testing and hardware setup</h2>

**Setup 1 (Physical device):**
- OS: Alma Linux 9.3 (Shamrock Pampas Cat)
- Kernel: 5.14.0-362.18.1.el9_3.x86_64
- Hardware memory type: SSD (~874 GB of storage available)
- RAM: 16 GB
- Processor: Intel i7-10750H (12) @ 5.000GHz

**Setup 2 (Virtual machine):**
- Host OS: Windows 10
- OS: Ubuntu 22.04
- Kernel: 5.14.0-362.18.1.el9_3.x86_64
- Hardware memory type: SSD (~120 GB of storage available)
- RAM: 8 GB of allocated host machine memory
- Processor: Intel i7-10750H (1) @ 2.592GHz 

**Setup 3 (Virtual machine):**
- Host OS: Windows 10
- OS: Alma Linux 8.9 (Midnight Oncilla)
- Kernel: 4.18.0-513.5.1.el8_9.x86_64 
- Hardware memory type: SSD (~120 GB of storage available)
- RAM: 8 GB of allocated host machine memory 
- Processor: Intel i7-10750H (1) @ 2.592GHz 

<h2>Results</h2>

Note: Benchmarking runs after the first time produce results similar to each other, but with slight difference to the first run.

<h3>chmod() results for setup 1 (Alma Linux 9):</h3>

First run of benchmarking script:
![alt text](/plots/alma_linux_9/100kb_35mb_range_1st_run.png)
Subsequent run of benchmarking script:
![alt text](/plots/alma_linux_9/100kb_35mb_range_2nd_run.png)

<h3>chmod() results for setup 2 (Ubuntu):</h3>

First run of benchmarking script:
![alt text](/plots/ubuntu/100kb_61mb_1st_run.png)
Subsequent run of benchmarking script:
![alt text](/plots/ubuntu/100kb_61mb_2nd_run.png)

<h3>chmod() results for setup 3 (Alma Linux 8):</h3>

First run of benchmarking script:
![alt text](/plots/alma_linux_8/100kb_35mb_range_1st_run.png)
Subsequent run of benchmarking script:
![alt text](/plots/alma_linux_8/100kb_35mb_range_2nd_run.png)

Obviously, there is only marginal increase in the performance on both the physical device and virtual machine running Alma Linux. But Ubuntu OS plot for regular OverlayFS setup demonstrates existing correlaction between file size and operation execution time. Moreover we can observe improvement with metacopy feature being turned on, but this speed-up is still not very significant from user's point of view as it influences benchmark at submiliseconds magnitude. 
On top of that, we can observe a small speed-up on the first run with metacopy feature being turned on (when no files from lower directore are presented in upper directory), but almost equal performance for regular and tuned setup of OverlayFS on susbsequent runs. 
There is a note at the bottom of metacopy feature paragraph in [OverlayFS docs](https://docs.kernel.org/filesystems/overlayfs.html):
```
Once the copy_up is complete, the overlay filesystem simply provides direct access to the newly created file
in the upper filesystem - future operations on the file are barely noticed by the overlay filesystem
(though an operation on the name of the file such as rename or unlink will of course be noticed and handled)
```
This note is quite obscure but seems like this is intended behavior in this case. Only the first run gets any speed-up.
Generally, I would not say that turning this feature on brings a lot of advantages but enabling it is very cheap and should not make experience unpleasant on the client's side, thus we can safely deploy it to the main software.
