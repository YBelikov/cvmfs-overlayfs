import os
from misc import list_absolute_file_paths
from optparse import OptionParser
import scienceplots
import matplotlib.pyplot as plt

def plot_results(paths, legend):
    plt.style.use(['science', 'no-latex', 'grid'])
    for path in paths:
        files = list_absolute_file_paths(path)
        for file in files:
            with open(file, 'r') as f:
                print(file)
                lines = f.readlines()
                x = [float(line.split()[0]) for line in lines]
                y = [float(line.split()[1]) for line in lines]
            plt.plot(x ,y)
    plt.legend(legend, loc='best')
    plt.xlabel('File size in bytes')  
    plt.ylabel('Average operation time in ms')            
    plt.show()

def main():
    usage = 'usage: <target path> [options]\n\
    This script plots a graph with benchmarking results acquired for baseline, overlayfs with features and regular overlayfs'
    parser = OptionParser(usage)
    parser.add_option('-t', '--path-to-base-res', dest='path_to_base_res', default='', help='Path to the file with baseline results')
    parser.add_option('-m', '--path-to-tuned-ovfs-res', dest='path_to_tuned_ovfs_res', default='', help='Path to the file with results for OVFS with features')
    parser.add_option('-r', '--path-to-regular-ovfs-res', dest='path_to_reg_ovfs_res', default = '', help='Path to the file with results for OVFS without features')
    
    (options, _) = parser.parse_args()
    
    try:
        path_to_base_res        = str(options.path_to_base_res)
        path_to_tuned_ovfs_res  = str(options.path_to_tuned_ovfs_res)
        path_to_reg_ovfs_res    = str(options.path_to_reg_ovfs_res)
    except ValueError:
        print('Cannot parse numerical options and/or parameters')
        exit(1)
    path_to_base_res = os.path.expanduser(path_to_base_res)
    path_to_tuned_ovfs_res = os.path.expanduser(path_to_tuned_ovfs_res)
    path_to_reg_ovfs_res = os.path.expanduser(path_to_reg_ovfs_res)
    plot_results([path_to_base_res, path_to_tuned_ovfs_res, path_to_reg_ovfs_res], ['base', 'ovlfs_metacopy', 'ovlfs_reg'])

if __name__ == '__main__':
    main()