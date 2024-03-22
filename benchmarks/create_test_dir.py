#!/usr/bin/env python

import os
import sys
import random
from optparse import OptionParser
from misc.log import *

BUFFER_SIZE=1048576
RANDOM_FILE_PREFIX="seeded_file"

def produce_dir(path, number_of_files, min_file_size, max_file_size):
    Logger.log(LogLevel.INFO, f'Seeding directory at path: {path}')
    os.makedirs(path, exist_ok=True)
    total_file_size = 0
    for i in range(number_of_files):
        target_file_path = os.path.join(path, f'{RANDOM_FILE_PREFIX}_{i}')
        total_file_size += create_random_file(target_file_path=target_file_path, min_size=min_file_size, max_size=max_file_size)
    return total_file_size

def seed_directory(path, max_directory_size):
    Logger.log(LogLevel.INFO, f'Seeding directory at path: {path}')
    os.makedirs(path, exist_ok=True)
    total_file_size = 0
    file_index = 1
    while total_file_size < max_directory_size:
        target_file_path = os.path.join(path, f'{RANDOM_FILE_PREFIX}_{file_index}')
        total_file_size += create_random_file(target_file_path=target_file_path, min_size=0, max_size=max_directory_size)
        file_index += 1
    return total_file_size

def create_random_file(target_file_path, min_size, max_size):
    file_size = random.randint(min_size, max_size)
    bytes_remaining = file_size
    with open(target_file_path, 'wb') as target_file:
        while bytes_remaining > 0:
            if bytes_remaining > BUFFER_SIZE:
                write_contents(target_file, BUFFER_SIZE)
                bytes_remaining -= BUFFER_SIZE
            else:
                write_contents(target_file, file_size)
                bytes_remaining = 0
    return file_size

def write_contents(file_stream, output_size):
    if sys.version_info.major >= 3 and sys.version_info.minor < 9:
        file_stream.write(random.getrandbits(8 * output_size).to_bytes(output_size, 'little'))
    else:
        file_stream.write(random.randbytes(output_size))

def main():
    #command line parameter parser setup
    usage = "usage: %prog [options] <destination path>\n\
    This creates dummy folder filled with files in the specified range."
    parser = OptionParser(usage)
    parser.add_option("-n", "--number-of-files",    dest="number_of_files",     default=100,    help="the number of files to be generated in the given directory")
    parser.add_option("-l", "--min-file-size",      dest="min_file_size",       default=0,      help="minimal file size for random file contents in bytes")
    parser.add_option("-u", "--max-file-size",      dest="max_file_size",       default=102400, help="maximal file size for random file contents in bytes")
 
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Please provide the mandatory arguments")
    try:
        number_of_files    = int(options.number_of_files)
        min_file_size      = int(options.min_file_size)
        max_file_size      = int(options.max_file_size)
    except ValueError:
        Logger.log(LogLevel.ERROR, "Cannot parse numerical options and/or parameters")
        exit(1)

    target_dir_path = args[0]
    produce_dir(path=target_dir_path, number_of_files=number_of_files, min_file_size=min_file_size, max_file_size=max_file_size)

if __name__ == '__main__':
    main()