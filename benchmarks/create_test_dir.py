#!/usr/bin/env python

import os
import random
from optparse import OptionParser

def log_error(message):
    print(f"[ERROR]: {message}")

def produce_dir(path, number_of_files, min_file_size, max_file_size, big_file_threshold):
    print("on dir producing")
    os.makedirs(path, exist_ok=True)
    file_prefix = ""  
    for i in range(number_of_files):
        file_size = random.randint(min_file_size, max_file_size)
        if file_size >= big_file_threshold:
            file_prefix = "big_file"
        else:
            file_prefix = "regular_file"
        target_file_path = "".join([path, '/', file_prefix, f'_{i}'])
        with open(target_file_path, '+wb') as target_file:
            target_file.write(random.randbytes(file_size))

def main():
    #command line parameter parser setup
    usage = "usage: %prog [options] <destination path>\n\
    This creates dummy file system content based on the parameters provided."
    parser = OptionParser(usage)
    parser.add_option("-n", "--number-of-files",     dest="number_of_files",     default=100,      help="the number of files to be generated in the given directory")
    parser.add_option("-l", "--min-file-size",     dest="min_file_size",     default=0,      help="minimal file size for random file contents in bytes")
    parser.add_option("-u", "--max-file-size",     dest="max_file_size",     default=102400, help="maximal file size for random file contents in bytes")
    parser.add_option("-t", "--big-file-threshold",   dest="big_file_threshold",   default=0.0,    help="threshold for the file to be considered big")

    # read command line arguments
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Please provide the mandatory arguments")
    try:
        number_of_files   = int(options.number_of_files)
        min_file_size     = int(options.min_file_size)
        max_file_size     = int(options.max_file_size)
        big_file_threshold = int(options.big_file_threshold)
    except ValueError:
        log_error("Cannot parse numerical options and/or parameters")
    target_dir_path = args[0]
    produce_dir(target_dir_path, number_of_files, min_file_size, max_file_size, big_file_threshold)

if __name__ == '__main__':
    main()