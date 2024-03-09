import os
from time import perf_counter

def chmod(file):
    start_time = perf_counter()
    os.chmod(file, 0o777)
    end_time = perf_counter()
    os.chmod(file, 0o644)
    # To get time in milliseconds
    return (end_time - start_time) * 1000

def chown(file):
    pass

if __name__ == '__main__':
   chmod('~/test')