#!/usr/bin/env python

import os
import matplotlib.pyplot as plt
from time import perf_counter
from optparse import OptionParser
from collections import defaultdict
from misc import Logger
from misc import LogLevel
from misc import list_absolute_file_paths

class OperationBenchmarkResult:
    def __init__(self, name, sizes, operations_times):
        self.name = name
        self.sizes = sizes
        self.operations_times = operations_times

def benchmark_chmod(file_path):
    start_time = perf_counter()
    os.chmod(file_path, 0o777)
    end_time = perf_counter()
    os.chmod(file_path, 0o644)

    # To get time in milliseconds
    return (end_time - start_time) * 1000

def benchmark_write(file_path):
    from random import randbytes
    random_bytes_to_write = 10
    with open(file_path, 'r+b') as f:
        start = perf_counter()
        f.write(randbytes(random_bytes_to_write))       
        end = perf_counter()
        f.flush()

    # To get time in milliseconds
    return (end - start) * 1000

# Runs command for each file in a given FS object: 
def benchmark_avg_chmod(file_system_object_path, number_of_runs):
    sizes = list()
    avg_times = list()
    sub_fs_objects = list_absolute_file_paths(file_system_object_path)
    if len(sub_fs_objects) == 0:
        Logger.log(LogLevel.ERROR, "No files in the provided base directory")
        exit(1)
    if os.path.isdir(sub_fs_objects[0]):
        for subdir in sub_fs_objects:
            absolute_file_paths = list_absolute_file_paths(subdir)
            sizes.append(os.stat(absolute_file_paths[0]).st_size)
            times_of_runs = 0.0
            for run_idx in range(number_of_runs):
                for file_path in absolute_file_paths:
                    times_of_runs += benchmark_chmod(file_path)
            avg_times.append(times_of_runs / number_of_runs)
    else:
        sizes_to_times = defaultdict(int)
        for run_idx in range(number_of_runs):
            for file in sub_fs_objects:
                file_size = os.stat(file).st_size
                sizes_to_times[file_size] += benchmark_chmod(file)
        for time_of_run in sizes_to_times.values():
            avg_times.append(time_of_run / number_of_runs)
        for size in sizes_to_times.keys():
            sizes.append(size)
    return OperationBenchmarkResult('chmod', sizes, avg_times)

def output_result(path_to_result, benchmark_result):
    full_file_path = os.path.join(path_to_result, f'{benchmark_result.name}.txt')
    x = benchmark_result.sizes
    y = benchmark_result.operations_times
    
    if len(x) != len(y):
        Logger.log(LogLevel.ERROR, f'Unable to save file, lengths of x and y are different. x: {len(x)}, y: {len(y)}')
    
    zipped_list = list(zip(x, y))
    # Sort the list of tuples by the x-coordinate
    sorted_list = sorted(zipped_list)
    x, y = zip(*sorted_list)
    
    with open(full_file_path, 'w') as f:
        for idx in range(len(x)):
            f.write(f'{x[idx]} {y[idx]}\n')


def main():
    usage = 'usage: <target path> [options]\n\
    This script generates a specified number of directories with a list of randomly filled files of specific sizes in each directory.'
    parser = OptionParser(usage)
    parser.add_option('-t', '--path-to-target-dir', dest='path_to_target_dir', help='Path to the target dir for benchmarking')
    parser.add_option('-n', '--number-of-runs', dest='number_of_runs', default=1, help='Number of operation repetetions per each file')
    parser.add_option('-r', '--path-to-result', dest='path_to_result', help='Path to the directory where files with results stored')
    (options, _) = parser.parse_args()
    try:
        path_to_target_dir      = os.path.expanduser(str(options.path_to_target_dir))
        number_of_runs          = int(options.number_of_runs)
        path_to_result          = os.path.expanduser(str(options.path_to_result))

    except ValueError:
        Logger.log(LogLevel.INFO,'Cannot parse numerical options and/or parameters')
    path_to_target_dir = os.path.expanduser(path_to_target_dir)
    path_to_result = (path_to_result)
    Logger.log(LogLevel.DEBUG, f'Target: {path_to_target_dir}')
    Logger.log(LogLevel.DEBUG, f'Target: {path_to_result}')
    if not os.path.isdir(path_to_target_dir):
        Logger.log(LogLevel.INFO,"Provide a path to a directory!")
    benchmark_result = benchmark_avg_chmod(path_to_target_dir, number_of_runs)
    if os.path.exists(path_to_target_dir):
        Logger.log(LogLevel.INFO, f'Making dir: {path_to_result}')
        os.makedirs(path_to_result, exist_ok=True)
    output_result(path_to_result, benchmark_result)

if __name__ == '__main__':
    main()