**This repository contains a variety of materials (source code, documentation bits, benchmarks and reports) related to exploitation of modern [OverlayFS](https://docs.kernel.org/filesystems/overlayfs.html) features in [CVMFS](https://github.com/cvmfs/cvmfs). The work was done during the course of CERN Ukrainian Students Remote Program.
Currently, the following features are under research:**
- [Metadata copy only (metacopy=on feature)](https://github.com/YBelikov/cvmfs-overlayfs/blob/main/METACOPY.md)
- Zero-copy directory renames

To get average time comparison chart you may follow steps described in METACOPY.md or launch run.py Python scripts that perfmors test directories setup, file generation, mounting OverlayFS with different configurations, average operation time measurement per each file size available in testing directories, plotting graphs and unmounting both OverlayFS setups (the last option is a configurable one, you want to keep the setup to repeat your benchmarking).
Be aware that this script launches mount/umount commands under sudo so you will have to provide your passwords at some point of script execution. On top of that this script doesn't perform cleanup if you won't specify --cleanup-directories=True, or -c True option.

**Features:**
- **Flexible File Size Configuration:** Set minimum and maximum file sizes to tailor the benchmarking to your specific testing needs.
- **Custom File Count:** Specify the exact number of files to be generated for benchmarking.
- **Configurable Directory Paths:** Define custom paths for baseline and OverlayFS directory structures.
- **Multiple Benchmark Runs:** Execute a defined number of operation runs for thorough performance analysis.
- **Benchmark Result Export:** Automatically stores benchmarking results to a specified output directory.


**Requirements:**

Before running the script, ensure you have Python installed on your system. The script is compatible with Python 3.9 and later (I have plans to make it available for Python 2.x).
To install required packages perform the following steps:
```
cd cvmfs-overlayfs
pip install -r requirements.txt
```
You can do this either for system-wide installation or for virtual environment.

**Supported options:**
```
Usage: run.py [options]

Options:
  -h, --help                   Show this help message and exit.
  -l, --min-file-size          Min file size for random file contents in bytes (default: 0).
  -u, --max-file-size          Max file size for random file contents in bytes (default: 10000000).
  -n, --number-of-files        Number of files to generate (default: 100).
  -b, --base-dir               Path to the regular directory for baseline benchmark (default: ~/base_dir).
  -r, --overlay-fs-regular-dir Path to the directory where overlay FS structure without additional mount params will be spanned (default: ~/ovlfs_regular).
  -f, --overlay-fs-tuned-dir   Path to directory where overlay FS structure with additional params will be spanned (default: ~/ovlfs_tuned).
  -t, --runs-num               Number of operation runs during benchmarking (default: 100).
  -o, --output-path            Path where files with benchmarking results are stored (default: ~/ovlfs_benchmark_output). 
```
**Examples:**

To generate 100 files with sizes ranging from 1000 to 5000 bytes in the default directories, and run the benchmark 500 times, you would use the following command:
```python
python run.py --min-file-size=1000 --max-file-size=5000 --number-of-files=100 --runs_num=500
```
