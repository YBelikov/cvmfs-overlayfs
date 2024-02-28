import sys
import os
import matplotlib.pyplot as plt
from setup_file_batches import launch_benchmarks_per_each_dir

def plot_benchmark_results(x, y):
    zipped_list = list(zip(x, y))

    # Sort the list of tuples by the x-coordinate
    sorted_list = sorted(zipped_list)
    x, y = zip(*sorted_list)
    print(f"X: {x}")
    plt.title("chmod benchmarking") 
    plt.xlabel('File sizes') 
    plt.ylabel('Avg time is msec')
    plt.plot(x, y, marker = 'o', c = 'g') 
    plt.show()

def main():
    path_to_test = sys.argv[1]
    if not os.path.isdir(path_to_test):
        print("provide a path to a directory!")
    dir_to_size = dict()
    for subdir in os.listdir(path_to_test):
        full_subdir_path = os.path.join(path_to_test, subdir)
        first_file = None
        full_file_path = None
        if os.path.isdir(full_subdir_path):
            first_file = os.listdir(full_subdir_path)[0]
            full_file_path = os.path.join(full_subdir_path, first_file)
            #size = os.stat(full_file_path).st_size 
            dir_to_size[full_subdir_path] = os.stat(full_file_path).st_size 
        elif os.path.isfile(full_subdir_path):
            full_file_path = full_subdir_path
        #print(f"Path: {full_file_path}. Size: {size}")
            dir_to_size[full_file_path] = os.stat(full_file_path).st_size 
    
    size_to_avg_time = launch_benchmarks_per_each_dir(dir_to_size)
    x = list(size_to_avg_time.keys())
    y = list(size_to_avg_time.values())  
    plot_benchmark_results(x, y)

if __name__ == '__main__':
    main()