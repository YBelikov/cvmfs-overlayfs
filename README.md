**This repository contains a variety of materials (source code, documentation bits, benchmarks and reports) related to exploitation of modern [OverlayFS](https://docs.kernel.org/filesystems/overlayfs.html) features in [CVMFS](https://github.com/cvmfs/cvmfs). The work was done during the course of CERN Ukrainian Students Remote Program.
Currently, the following features are under research:**
- [Metadata copy only (metacopy=on feature)](https://github.com/YBelikov/cvmfs-overlayfs/blob/main/METACOPY.md)
- Zero-copy directory renames

To get average time comparison chart you may follow steps similar to the described in [METACOPY.md](https://github.com/YBelikov/cvmfs-overlayfs/blob/main/METACOPY.md) but running each script by yourself as well as do mounting/unmounting routine or launch run.py script that perfmors the following:
1. **Testing directories setup:** on this step the script creates regular directory for baseline measurements, and two separate directories to spawn OverlayFS directory structure (readonly lower layer directory, read-write upper layer directory, merge directory and work directory (scratch area for internal work of OverlayFS)) for mounting regular and tuned (with additional features enabled) filesystems respectively.   
2. **File generation:** generates specified number of files in the specified size range (in bytes, at least for now) in baseline directory and copies these files to lower layer directories for each OverlayFS setup
3. **Mounts OverlayFS with different configurations in the created mountpoints** (regular and tuned), requires **sudo** that's why the script may ask your password
4. **Average operation time measurement** per each file of a certain size available in testing directories: please, define functions you want to benchmark in [ops_to_benchmark.py](https://github.com/YBelikov/cvmfs-overlayfs/blob/improvements/benchmarks/ops_to_benchmark.py)
5. **Saving benchmarking results as text files**: corresponding benchmarking results that represent average ops execution time per a file in each testing directory (baseline directory, regular OverlayFS merge one, and merge directory in tuned OverlayFS) are written to the specified by script's options directory in the following format: ```file_size average_time_in_ms``` per line. Benchmarking result per each directory is stored in the separate subdirectory of the output one. 
6. **Plotting comparison graphs**: the script calls helper function from plot_comparison.py to draw a comparison plot per each operation

<h3>TODO:</h3>

- [x] **Unmounting OverlayFS**: add a key to run.py options for specifying whether OverlayFS setup should be unmounted at the end.
- [x] **Testing directories cleanup**: add a key to run.py options for specifying whether directories used in benchmarking should be removed from local FS.
- [x] **Ability to pass any other function to measure it's performance on the given filesystem setup**
- [ ] **Script steps to deal with outliers in data**
- [ ] **Replace os API usage with Pathlib?**

Be aware that this script launches mount/umount commands under sudo so you will have to provide your passwords at some point of script execution.

**Features:**
- **Flexible File Size Configuration:** Set minimum and maximum file sizes to tailor the benchmarking to your specific testing needs.
- **Custom File Count:** Specify the exact number of files to be generated for benchmarking.
- **Configurable Directory Paths:** Define custom paths for baseline and OverlayFS directory structures.
- **Multiple Benchmark Runs:** Execute a defined number of operation runs for thorough performance analysis.
- **Benchmark Result Export:** Automatically stores benchmarking results to a specified output directory.

**Prerequisities:**

Before running the script, ensure you have Python installed on your system. The script is compatible with Python 3.x.
To install required packages perform the following steps:
```
cd cvmfs-overlayfs
pip install -r requirements.txt
```
You can do this either for system-wide installation or for virtual environment.
However, plotting uses matplotlib, thus you should have some compatible GUI backend installed on your system (it could be Tkinter or PyQT). 
Personally, I prefer Tkinter, so I leave here an installation line:

**For Ubuntu:**
```
sudo apt-get install python3-tk
```
**For Alma Linux:**
```
sudo dnf install python3-tkinter
```
**Supported options:**
```
Usage: run.py [options]

Options:
--min-file-size          Minimum file size for random file contents in bytes (default: 0).
--max-file-size          Maximum file size for random file contents in bytes (default: 10000000).
--number-of-files        Number of files to generate (default: 100).
--base-dir               Path to the regular directory for baseline benchmark (default: ~/base_dir).
--overlay-fs-regular-dir Path to the directory where overlay FS structure without additional mount params will be spanned (default: ~/ovlfs_regular).
--overlay-fs-tuned-dir   Path to the directory where overlay FS structure with additional params will be spanned (default: ~/ovlfs_tuned).
--runs_num               Number of operation runs during benchmarking (default: 100).
--output-path            Path where files with benchmarking results are stored (default: ~/ovlfs_benchmark_output).
--unmount-ovlfs          Specifies the need to unmount overlay filesystems after benchmarking (default: False).
--delete-files           Specifies the need to delete seeded files and directories at the end of run (default: False).
--relaunch-benchmark     Specifies the need to relaunch benchmark using provided directories (default: False).
```
**Examples:**

To generate 100 files with sizes ranging from 1000 to 5000 bytes in the default directories, and run the benchmark 500 times, you would use the following command:
```python
python run.py --min-file-size=1000 --max-file-size=5000 --number-of-files=100 --runs_num=500
```
