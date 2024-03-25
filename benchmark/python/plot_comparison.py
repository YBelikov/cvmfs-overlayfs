#!/usr/bin/env python

import os
from pathlib import Path
from misc import list_absolute_file_paths, Logger, LogLevel
from optparse import OptionParser
import scienceplots
import matplotlib.pyplot as plt

def plot_results(path):
    plt.style.use(['science', 'no-latex', 'grid'])
    for fs_object in list_absolute_file_paths(path):
        if os.path.isdir(fs_object):
            plt.figure()
            legend = list()
            for file in list_absolute_file_paths(fs_object):
                Logger.log(LogLevel.DEBUG, f'Path: {file}')
                with open(file, 'r') as f:
                    lines = f.readlines()
                    x = [float(line.split()[0]) for line in lines]
                    y = [float(line.split()[1]) for line in lines]
                    legend.append(Path(file).stem)
                    plt.plot(x, y)
            plt.legend(legend, loc='best')
            plt.xlabel('File size in bytes')  
            plt.ylabel('Average operation time in ms') 
            plt.title(f'{os.path.basename(fs_object)} benchmark results')                     
    plt.show()

def main():
    usage = 'usage: <target path> [options]\n\
    This script plots a graph with benchmarking results acquired for baseline, overlayfs with features and regular overlayfs'
    parser = OptionParser(usage)
    parser.add_option('--path-to-base-res', dest='path_to_base_res', default='', help='Path to the file with baseline results')
    (options, _) = parser.parse_args()
    
    try:
        path_to_base_res = str(options.path_to_base_res)
    except ValueError:
        print('Cannot parse numerical options and/or parameters')
        exit(1)
    path_to_base_res = os.path.expanduser(path_to_base_res)
    plot_results(path_to_base_res)

if __name__ == '__main__':
    main()