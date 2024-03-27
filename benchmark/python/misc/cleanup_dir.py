#!/usr/bin/env python

import os
import shutil
import sys
from log import *
from utils import list_absolute_file_paths
 
def cleanup_dir(target_dir):
    if not os.path.isdir(target_dir):
        Logger.log(LogLevel.ERROR, "Please, provide path to the directory as a command line argument. Non-directory detected as an parameter")
        raise ValueError(f'Provided path does not point to a directory: {target_dir}')   
    
    files_to_remove = list_absolute_file_paths(target_dir)
    for file in files_to_remove:
        if os.path.isdir(file):
            shutil.rmtree(file)
        else:
            os.remove(file)

def remove_dir(target_dir):
    if not os.path.isdir(target_dir):
        Logger.log(LogLevel.ERROR, "Please, provide path to the directory as a command line argument. Non-directory detected as an parameter")
        raise ValueError(f'Provided path does not point to a directory: {target_dir}')
    shutil.rmtree(target_dir) 

def main():
    if len(sys.argv) != 2:
        Logger.log(LogLevel.ERROR, "Please, provide path to the directory as a command line argument")
        exit(1)
    target_dir = sys.argv[1]
    cleanup_dir(target_dir)

if __name__ == '__main__':
    main()