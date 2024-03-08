#!/usr/bin/env python

import shutil
import sys
from .log import *

def copy_dir(source, dest):
    shutil.copytree(source, dest, dirs_exist_ok=True)
    
def main():
    if len(sys.argv) != 3:
        Logger(LogLevel.ERROR, "Provide source and destination paths")
        exit(1)
    source = sys.argv[1]
    destination = sys.argv[2]
    try:
        copy_dir(source, destination)
    except Exception as ex:
        Logger.log(LogLevel.ERROR, f"{ex}")
        exit(1)
        
if __name__ == '__main__':
    main()