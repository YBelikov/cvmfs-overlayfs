#!/usr/bin/env python

import os
import matplotlib.pyplot as plt
from ops_to_benchmark import chmod, move_directory
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

class Operation:
    def __init__(self, condition, func):
        self.condition = condition
        self.func = func

def calc_dir_size(dir):
    total_size = 0
    directory_contents = list_absolute_file_paths(dir)
    for file in directory_contents:
        if os.path.isfile(file):
            total_size += os.stat(file).st_size
        else:
            total_size += calc_dir_size(file)
    return total_size

# Runs command for each file in a given FS object: 
def benchmark_walk_tree_avg(file_system_object_path, number_of_runs, operation):
    sizes = list()
    avg_times = list()
    with os.scandir(file_system_object_path) as it:
        for entry in it:
            times_of_runs = 0
            if entry.is_dir():
                if not operation.condition(entry.path):
                    continue
                sizes.append(calc_dir_size(entry.path))
                for _ in range(number_of_runs):
                    times_of_runs += operation.func(entry.path)  
                avg_times.append(times_of_runs / number_of_runs)
                benchmark_walk_tree_avg(file_system_object_path=entry.path, number_of_runs=number_of_runs, operation=operation)
            if entry.is_file():
                file_size = os.stat(entry.path).st_size
                sizes.append(file_size)
                for _ in range(number_of_runs):
                    times_of_runs += operation.func(entry.path)
                avg_times.append(times_of_runs / number_of_runs)
    return OperationBenchmarkResult(operation.func.__name__, sizes, avg_times)

def output_result(path_to_result, type, benchmark_result):
    path_to_command_results = os.path.join(path_to_result, benchmark_result.name)
    os.makedirs(path_to_command_results, exist_ok=True)
    full_file_path = os.path.join(path_to_command_results, f'{type}.txt')
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
    parser.add_option('--path-to-target-dir', dest='path_to_target_dir', help='Path to the target dir for benchmarking')
    parser.add_option('--number-of-runs', dest='number_of_runs', default=1, help='Number of operation repetetions per each file')
    parser.add_option('--path-to-result', dest='path_to_result', help='Path to the directory where files with results stored')
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

    op_to_test = Operation(condition=lambda s: os.path.isdir(s), func=move_directory)
    benchmark_result = benchmark_walk_tree_avg(path_to_target_dir, number_of_runs, op_to_test)
    if os.path.exists(path_to_target_dir):
        Logger.log(LogLevel.INFO, f'Making dir: {path_to_result}')
        os.makedirs(path_to_result, exist_ok=True)
    output_result(path_to_result, 'baseline', benchmark_result)

if __name__ == '__main__':
    main()