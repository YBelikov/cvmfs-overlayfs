#!/usr/bin/env python

import os
import sys
import random
from optparse import OptionParser
from misc.log import *

def produce_dir(path, number_of_files, min_file_size, max_file_size):
    Logger.log(LogLevel.INFO, f'Seeding directory at path: {path}')
    # 2^30 just arbitrary large number of bytes that could be written with randbytes without C-int overflow 
    buffer_size = 1048576 
    os.makedirs(path, exist_ok=True)
    file_prefix = "seeded_file"  
    total_file_size = 0
    for i in range(number_of_files):
        file_size = random.randint(min_file_size, max_file_size)
        total_file_size += file_size
        target_file_path = os.path.join(path, f'{file_prefix}_{i}')
        with open(target_file_path, 'wb') as target_file:
            while file_size > 0:
                if file_size > buffer_size:
                    write_to_file(target_file, buffer_size)
                    file_size -= buffer_size
                else:
                    write_to_file(target_file, file_size)
                    file_size = 0
    return total_file_size

def write_to_file(file_stream, output_size):
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
    produce_dir(target_dir_path, number_of_files, min_file_size, max_file_size)

if __name__ == '__main__':
    main()