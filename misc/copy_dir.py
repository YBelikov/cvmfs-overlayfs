import shutil
import sys
from log import log_error

def main():
    if len(sys.argv) != 3:
        log_error("Provide source and destination paths")
    source = sys.argv[1]
    destination = sys.argv[2]
    try:
        shutil.copytree(source, destination, dirs_exist_ok=True)
    except Exception as ex:
        log_error(f"{ex}")
        
if __name__ == '__main__':
    main()