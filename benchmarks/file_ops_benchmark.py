import os
import time 
from optparse import OptionParser
from timeit import timeit

def log_error(message):
    print(f"[ERROR]: {message}")

def list_absolute_file_paths(path):
    return [os.path.join(path, file) for file in os.listdir(path)]
 
def benchmark_chmod(files_list):
    total_exec_time = 0.0
    for filepath in files_list:
        start = time.perf_counter()
        os.chmod(filepath, 0o777)
        end = time.perf_counter()
        total_exec_time += (start - end)
    for filepath in files_list:
        start = time.perf_counter()
        os.chmod(filepath, 0o644)
        end = time.perf_counter()
        total_exec_time += (start - end)
    return total_exec_time
    
def average(list_of_values):
    return sum(list_of_values) / len(list_of_values)

def main():
    usage = "usage: %prog [options] <destination path>\n\
    This creates dummy file system content based on the parameters provided."
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

    files_list = list_absolute_file_paths(path)
    results = [benchmark_chmod(files_list) for i in range(test_suites)]    
    avg = average(results)
    print('=================================')
    print(f'Average execution time: {avg}s')

if __name__ == '__main__':
    main()
    