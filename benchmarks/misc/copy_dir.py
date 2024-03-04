#!/usr/bin/env python

import shutil
import sys
from log import *

def main():
    if len(sys.argv) != 3:
        Logger(LogLevel.ERROR, "Provide source and destination paths")
        exit(1)
    source = sys.argv[1]
    destination = sys.argv[2]
    try:
        shutil.copytree(source, destination, dirs_exist_ok=True)
    except Exception as ex:
        Logger.log(LogLevel.ERROR, f"{ex}")
        exit(1)
        
if __name__ == '__main__':
    main()