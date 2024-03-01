import os
import shutil
import sys
from log import log_error

def list_absolute_file_paths(path):
    return [os.path.join(path, file) for file in os.listdir(path)]
 
def main():
    if len(sys.argv) != 2:
        log_error("Please, provide path to the directory as a command line argument")
        exit(1)
    
    target_dir = sys.argv[1]
    
    if not os.path.isdir(target_dir):
        log_error("Please, provide path to the directory as a command line argument. Non-directory detected as an parameter")
        exit(1)    
    
    files_to_remove = list_absolute_file_paths(target_dir)
    for file in files_to_remove:
        if os.path.isdir(file):
            shutil.rmtree(file)
        else:
            os.remove(file)

if __name__ == '__main__':
    main()