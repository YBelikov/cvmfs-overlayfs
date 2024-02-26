#!/usr/bin/env python
import os
import matplotlib.pyplot as plt
from create_test_dir import produce_dir
from file_ops_benchmark import benchmark_chmod_avg

from optparse import OptionParser

def log_error(message):
    print(f"[ERROR]: {message}")

def setup_dir_structure(base_dir, number_of_directories, number_of_files, lower_size_bound, upper_size_bound):
    dir_name_pattern = "batch_dir"
    size_interval = upper_size_bound - lower_size_bound
    size_step = size_interval // number_of_directories
    dir_to_size_dict = dict()
    for i in range(number_of_directories):
        dir_path = "".join([base_dir, '/', dir_name_pattern, f'_{i}']) #os.path.join([base_dir, dir_name_pattern, f'_{(i+1)}'])
        if os.path.exists(dir_path):
            continue
        os.makedirs(dir_path)
        size_in_dir = lower_size_bound + i * size_step
        produce_dir(dir_path, number_of_files, size_in_dir, size_in_dir, size_in_dir)
        dir_to_size_dict[dir_path] = size_in_dir
    return dir_to_size_dict

def launch_benchmarks_per_each_dir(dir_to_size_dict):
    size_to_avg_chown = dict()
    for dir in dir_to_size_dict.keys():
        result = benchmark_chmod_avg(dir, 1000)
        size_to_avg_chown[dir_to_size_dict[dir]] = result
    return size_to_avg_chown

def plot_benchmark_results(size_to_avg_time):
    x = list(size_to_avg_time.keys())
    y = list(size_to_avg_time.values())      
    plt.title("chmod benchmarking") 
    plt.xlabel('File sizes') 
    plt.ylabel('Avg time is sec') 
    plt.yticks(y) 
    plt.plot(x, y, marker = 'o', c = 'g') 
    plt.show()

def main():
    usage = 'usage: <target path> [options]\n\
    This script generates a specified number of directories with a list of randomly filled files of specific sizes in each directory.'
    parser = OptionParser(usage)
    parser.add_option('-d', '--number-of-directories', dest='number_of_directories', default=1, help='Number of directories to be generated (number of chosen size-points) in the specified range')
    parser.add_option('-f', '--number-of-files', dest='number_of_files', default=1, help='Number of files per each directory')
    parser.add_option('-l', '--lower-size-bound', dest='lower_size_bound', default=0, help='The lower bound of the size interval')
    parser.add_option('-u', '--upper-size-bound', dest='upper_size_bound', default=1000000, help='The uper bound of the size interval')
    (options, args) = parser.parse_args()
    try:
        number_of_directories   = int(options.number_of_directories)
        number_of_files         = int(options.number_of_files)
        lower_size_bound        = int(options.lower_size_bound)
        upper_size_bound        = int(options.upper_size_bound)
    except ValueError:
        log_error("Cannot parse numerical options and/or parameters")
    base_dir = args[0]
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # TODO: Add preliminary check on the availability of disk space before running this script
    dir_to_size = setup_dir_structure(base_dir, number_of_directories, number_of_files, lower_size_bound, upper_size_bound)
    size_to_avg_time = launch_benchmarks_per_each_dir(dir_to_size)
    plot_benchmark_results(size_to_avg_time)

if __name__ == '__main__':
    main()