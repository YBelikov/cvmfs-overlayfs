import os
import shutil
from misc.utils import system
from time import perf_counter
from pathlib import Path

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


def cpp_chmod(input_path, output_path):
    system(f'../cpp_benchmark_ops/benchmark_chmod 1000 {input_path} {output_path}')

def cpp_update_time(input_path, output_path):
    system(f'../cpp_benchmark_ops/bin/benchmark 1000 {input_path} {output_path}')

def touch_pathlib(file):
    pathlib_converted_file = Path(file)
    start_time = perf_counter()
    pathlib_converted_file.touch()
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

def move_directory(file):
    if not os.path.isdir(file):
        return 0.0
    start_time = perf_counter()
    shutil.move(src=file, dst=f'{file}_renamed')
    end_time = perf_counter()

    # To leave directories original names intact 
    shutil.move(src=f'{file}_renamed', dst=file)
    return (end_time - start_time) * 1000

if __name__ == '__main__':
   chmod('~/test')