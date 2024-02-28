#!/usr/bin/env python

import os
import time 
import random
from optparse import OptionParser
from timeit import timeit

def log_error(message):
    print(f"[ERROR]: {message}")

def list_absolute_file_paths(path):
    return [os.path.join(path, file) for file in os.listdir(path)]

def benchmark_chown(files_list):
    return 0

def benchmark_chmod(files_list):
    total_exec_time = 0.0
    for filepath in files_list:
        start = time.perf_counter()
        os.chmod(filepath, 0o777)
        end = time.perf_counter()
        
        # Get execution time in ms
        total_exec_time += (end - start) * 1000 

    # Just setting file modes back to -rw-r--r--  
    for filepath in files_list:
        os.chmod(filepath, 0o644)
    return total_exec_time

def benchmark_chmod_avg(path, test_suites):
    chmod_results = list()
    if os.path.isdir(path):
        files_list = list_absolute_file_paths(path)
    elif os.path.isfile(path):
        files_list = [path]
    chmod_results = [benchmark_chmod(files_list) for i in range(test_suites)] 
    chmod_avg = average(chmod_results)
    return chmod_avg

def benchmark_write_avg(path, test_suites):
    files_list = list_absolute_file_paths(path)
    write_results = [benchmark_write(files_list) for i in range(test_suites)]
    write_avg = average(write_results)
    return write_avg

def benchmark_write(files_list):
    total_exec_time = 0.0
    for filepath in files_list:
        with open(filepath, 'r+b') as f:
            f.seek(0)
            start = time.perf_counter()
            # Write the new byte
            f.write(random.randbytes(1))       
            end = time.perf_counter()
            f.flush()
            total_exec_time += (end - start)
    return total_exec_time

def average(list_of_values):
    return sum(list_of_values) / len(list_of_values)

def main():
    usage = "usage: %prog [options] <destination path>\n\
    This script performs benchmarking of chown and write calls on a list of files in a specified directory"
    parser=OptionParser(usage)
    parser.add_option("-c", "--cases", dest="test_suites", default=100, help='number of benchmark tests repetition')
    
    (options, args) = parser.parse_args()
    
    if len(args) != 1:
        log_error("Provide the required args!")
        exit(1)
    
    try:
        test_suites = int(options.test_suites)
    except ValueError:
        log_error("Cannot parse numerical options and/or parameters")
    path = args[0]
    
    if not os.path.isdir(path):
        log_error("Provide a path to directory")
        exit(1)
    
    if len(os.listdir(path)) == 0:
        log_error("Provide a non-empty directory")
        exit(1)
    
    chmod_avg = benchmark_chmod_avg(path, test_suites)
    write_avg = benchmark_write_avg(path, test_suites)
    
    print('=================================')
    print(f'Average execution time chmod: {chmod_avg}s')
    print(f'Average execution time write: {write_avg}s')

if __name__ == '__main__':
    main()
    