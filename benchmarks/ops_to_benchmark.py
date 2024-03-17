import os
from time import perf_counter

def chmod(file):
    start_time = perf_counter()
    os.chmod(file, 0o777)
    end_time = perf_counter()
    os.chmod(file, 0o644)
    # To get time in milliseconds
    return (end_time - start_time) * 1000

def read(file):
    with open(file, 'rb') as f:
        start_time = perf_counter()
        f.read(10)
        end_time = perf_counter()
    return (end_time - start_time) * 1000

def rename_directory(file):
    if not os.path.isdir(file):
        return 0.0
    start_time = perf_counter()
    os.rename(file, f'{file}_renamed')
    end_time = perf_counter()

    # To leave directories original names intact 
    os.rename(f'{file}_renamed', file)
    return (end_time - start_time) * 1000

if __name__ == '__main__':
   chmod('~/test')