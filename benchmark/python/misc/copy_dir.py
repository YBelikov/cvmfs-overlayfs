#!/usr/bin/env python

import shutil
import sys
import os
from .log import *

def copy_dir(source, dest):
    if sys.version_info.major >=3 and sys.version_info.minor < 8:
        copytree(source, dest)
        return 
    shutil.copytree(source, dest, dirs_exist_ok=True)

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

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