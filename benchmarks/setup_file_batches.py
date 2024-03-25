#!/usr/bin/env python

import os
from misc import Logger, LogLevel
from create_test_dir import produce_dir
from optparse import OptionParser

def setup_batch(base_dir, number_of_directories, lower_size_bound, upper_size_bound):
    dir_name_pattern = "batch_dir"
    size_interval = upper_size_bound - lower_size_bound
    size_step = size_interval // number_of_directories
    for i in range(number_of_directories):
        dir_path = os.path.join(base_dir, dir_name_pattern)
        dir_path += f'_{(i+1)}'
        total_dir_size = lower_size_bound + i * size_step
        if total_dir_size > size_interval:
            total_dir_size = total_dir_size - size_interval
            size_interval = 0
        else:
            size_interval -= total_dir_size
        if os.path.exists(dir_path):
            continue
        os.makedirs(dir_path)
        # Produce subdirectory with files of equal size
        produce_dir(path=dir_path, max_directory_size=total_dir_size)
    return

def main():
    usage = 'usage: <target path> [options]\n\
    This script generates a specified number of directories with a list of randomly filled files of specific sizes in each directory.'
    parser = OptionParser(usage)
    parser.add_option('-d', '--number-of-directories', dest='number_of_directories', default=1, help='Number of directories to be generated (number of chosen size-points) in the specified range')
    parser.add_option('-l', '--lower-size-bound', dest='lower_size_bound', default=0, help='The lower bound of the size interval')
    parser.add_option('-u', '--upper-size-bound', dest='upper_size_bound', default=1000000, help='The uper bound of the size interval')
    (options, args) = parser.parse_args()
    try:
        number_of_directories   = int(options.number_of_directories)
        lower_size_bound        = int(options.lower_size_bound)
        upper_size_bound        = int(options.upper_size_bound)
    except ValueError:
        Logger.log(LogLevel.ERROR, "Cannot parse numerical options and/or parameters")
        exit(1)
        
    base_dir = os.path.expanduser(args[0])
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # TODO: Add preliminary check on the availability of disk space before running this script
    setup_batch(base_dir, number_of_directories, lower_size_bound, upper_size_bound)

if __name__ == '__main__':
    main()