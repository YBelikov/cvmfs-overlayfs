#!/usr/bin/env python

# Sole purpose of this script is to provide the single entry point for anyone who wants to run get plots without need to 
# launch each separate script separately
# Definetely, anyone can use scripts from this repo as standalone without running this script

import os
from ops_to_benchmark import chmod, read, rename_directory, move_directory, cpp_chmod, cpp_update_time
from optparse import OptionParser
from misc.log import *
from create_test_setup import produce_dir
from misc.copy_dir import copy_dir
from misc.utils import system
from plot_comparison import plot_results
from perform_benchmarks import benchmark_walk_tree_avg
from setup_file_batches import setup_batch
from pathlib import Path

OVLFS_LOWER_DIR='lower'
OVLFS_UPPER_DIR='upper'
OVLFS_MERGE_DIR='merge'
OVLFS_WORK_DIR='work'
BASELINE_RESULT_FILE_NAME='baseline.txt'
TUNED_OVLFS_RESULT_FILE_NAME='tuned.txt'
REGULAR_OVLFS_RESULT_FILE_NAME='regular.txt'

def seed_test_dirs(min_file_size, max_file_size, files_num, base_dir, ovlfs_reg_dir, ovlfs_tuned_dir, seed_batch=False, dirs_in_batch=1):
    if seed_batch and dirs_in_batch == 0:
        Logger.log(LogLevel.ERROR, f'If seed_batch provided as True specify the number of directories > 0: {ex}')
        exit(1)
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(ovlfs_reg_dir, exist_ok=True)
    os.makedirs(ovlfs_tuned_dir, exist_ok=True)
    for ovlfs_dir in [ovlfs_reg_dir, ovlfs_tuned_dir]:
        os.makedirs(os.path.join(ovlfs_dir, OVLFS_LOWER_DIR), exist_ok=True)
        os.makedirs(os.path.join(ovlfs_dir, OVLFS_UPPER_DIR), exist_ok=True)
        os.makedirs(os.path.join(ovlfs_dir, OVLFS_MERGE_DIR), exist_ok=True)
        os.makedirs(os.path.join(ovlfs_dir, OVLFS_WORK_DIR), exist_ok=True)
    if seed_batch:
        setup_batch(base_dir=base_dir, number_of_directories=dirs_in_batch, lower_size_bound=min_file_size, upper_size_bound=max_file_size)
    else:        
        produce_dir(base_dir, files_num, min_file_size, max_file_size)
    try:
        Logger.log(LogLevel.INFO, f'Copying directory: {os.path.join(ovlfs_reg_dir, OVLFS_LOWER_DIR)}')
        copy_dir(base_dir, os.path.join(ovlfs_reg_dir, OVLFS_LOWER_DIR))
        Logger.log(LogLevel.INFO, f'Copying directory: {os.path.join(ovlfs_tuned_dir, OVLFS_LOWER_DIR)}')
        copy_dir(base_dir, os.path.join(ovlfs_tuned_dir, OVLFS_LOWER_DIR))
    except ValueError as ex:
        Logger.log(LogLevel.ERROR, f'Error on copying base directory contents: {ex}')

def mount_filesystems(ovlfs_reg_dir, ovlfs_tuned_dir, metacopy, redirect_dir):
    Logger.log(LogLevel.INFO, 'Mounting seeded filesystems')
    options = ''
    if metacopy:
        options += 'metacopy=on,'
    if redirect_dir:
        options += 'redirect_dir=on'
    system(f'sudo mount -t overlay overlay -o lowerdir={os.path.join(ovlfs_tuned_dir, OVLFS_LOWER_DIR)},upperdir={os.path.join(ovlfs_tuned_dir, OVLFS_UPPER_DIR)},workdir={os.path.join(ovlfs_tuned_dir, OVLFS_WORK_DIR)},{options} {os.path.join(ovlfs_tuned_dir, OVLFS_MERGE_DIR)}')
    system(f'sudo mount -t overlay overlay -o lowerdir={os.path.join(ovlfs_reg_dir, OVLFS_LOWER_DIR)},upperdir={os.path.join(ovlfs_reg_dir, OVLFS_UPPER_DIR)},workdir={os.path.join(ovlfs_reg_dir, OVLFS_WORK_DIR)} {os.path.join(ovlfs_reg_dir, OVLFS_MERGE_DIR)}')

def unmount_filesystems(ovlfs_reg_dir, ovlfs_tuned_dir):
    Logger.log(LogLevel.INFO, 'Unmounting seeded filesystems')
    system(f'sudo umount {os.path.join(ovlfs_reg_dir, OVLFS_MERGE_DIR)}')
    system(f'sudo umount {os.path.join(ovlfs_tuned_dir, OVLFS_MERGE_DIR)}')

def run_benchmark(target_dir, runs_num, benchmark_func):
    Logger.log(LogLevel.INFO, f'Running benchmark on {target_dir} for {benchmark_func.__name__}')
    return benchmark_walk_tree_avg(target_dir, runs_num, benchmark_func)

def create_output_dirs(output_path):
    os.makedirs(output_path, exist_ok=True)

def delete_seeded_files(baseline_path, tuned_ovlfs_path, regular_ovlfs_path):
    Logger.log(LogLevel.INFO, 'Removing seeded directories')
    system(f'sudo rm -rf {baseline_path}')
    system(f'sudo rm -rf {tuned_ovlfs_path}')
    system(f'sudo rm -rf {regular_ovlfs_path}')

def main():
    usage = 'usage: <target path> [options]\n\
    This script plots a graph with benchmarking results acquired for baseline, overlayfs with features and regular overlayfs'
    parser = OptionParser(usage)
    parser.add_option('--min-file-size', dest='min_file_size', default=0, help='Min file size for random file contents in bytes')
    parser.add_option('--max-file-size', dest='max_file_size', default=10000000, help='Max file size for random file contents in bytes')
    parser.add_option('--number-of-files', dest='files_num', default=100, help='Number of files to generate')
    parser.add_option('--seed-directories-batch', dest='seed_directories_batch', default=False, help='Number of directories to generate and fill with files in a --base-dir')
    parser.add_option('--dirs-in-batch', dest='dirs_in_batch', default=0, help='In a case of --seed-directories-batch=True, specifies the number of dirs in a generated batch')
    parser.add_option('--base-dir', dest='base_dir', default='~/base_dir', help='Path to the regular directory for baseline benchmark')
    parser.add_option('--overlay-fs-regular-dir', dest='ovlfs_reg_dir', default ='~/ovlfs_regular', help='Path to the directory where overlay FS structure without additional mount params will be spanned')
    parser.add_option('--overlay-fs-tuned-dir', dest='ovlfs_tuned_dir', default = '~/ovlfs_tuned', help='Path to directory where overlay FS structure with additional params will be spanned')
    parser.add_option('--redirect-dir', dest='redirect_dir', default = False, help='redirect_dir config option state for overlayfs mount')
    parser.add_option('--metacopy', dest='metacopy', default = False, help='metacopy config option state for overlayfs mount') 
    parser.add_option('--runs-num', dest='runs_num', default = 100, help='Number of operation runs during benchmarking')
    parser.add_option('--output-path', dest='output_path', default = '~/ovlfs_benchmark_output', help='Path where files with benchmarking results are stored')
    parser.add_option('--unmount-ovlfs', dest='unmount_ovlfs', default = False, help='Specifies the need to unmount ovelray filesystems')
    parser.add_option('--delete-files', dest='delete_files', default = False, help='Specifies the need to delete seeded files and directories at the end of run')
    parser.add_option('--relaunch-benchmark', dest='relaunch_benchmark', default = False, help='Specifies the need to relaunch benchmark using provided directories')

    (options, _) = parser.parse_args()
    
    try:
        min_file_size           = int(options.min_file_size)
        max_file_size           = int(options.max_file_size) 
        files_num               = int(options.files_num)
        seed_directories_batch  = bool(options.seed_directories_batch)
        dirs_in_batch           = int(options.dirs_in_batch)
        base_dir                = str(options.base_dir)
        ovlfs_reg_dir           = str(options.ovlfs_reg_dir)
        ovlfs_tuned_dir         = str(options.ovlfs_tuned_dir)
        redirect_dir            = bool(options.redirect_dir)
        metacopy                = bool(options.metacopy)
        runs_num                = int(options.runs_num)
        output_path             = str(options.output_path)
        unmount_ovlfs           = bool(options.unmount_ovlfs)
        delete_files            = bool(options.delete_files)
        relaunch_benchmark      = bool(options.relaunch_benchmark)
 
    except ValueError:
        print('Cannot parse numerical options and/or parameters')
        exit(1)
    if not unmount_ovlfs and delete_files:
        Logger.log(LogLevel.ERROR, 'You provided conflicting options for unmounting and deleting data. You have to unmount overlayfs before cleanup')
        exit(1)

    if not redirect_dir and metacopy:
        Logger.log(LogLevel.ERROR, 'You provided conflicting options for overlayfs mount. You should use redirect_dir=True in a case of metacopy=True')
        exit(1)
    
    if max_file_size < min_file_size:
        Logger.log(LogLevel.ERROR, 'Max file size must be bigger than min file size!')
        exit(1)
    
    if files_num <= 0:
        Logger.log(LogLevel.ERROR, 'You should provide positive number of files!')
        exit(1)

    if runs_num <= 0:
        Logger.log(LogLevel.ERROR, 'You should provide positive number of test runs!')
        exit(1)
    
    base_dir = os.path.expanduser(base_dir)
    ovlfs_reg_dir = os.path.expanduser(ovlfs_reg_dir)
    ovlfs_tuned_dir = os.path.expanduser(ovlfs_tuned_dir)
    output_path = os.path.expanduser(output_path)  
    if not relaunch_benchmark:
        if seed_directories_batch:
            seed_test_dirs(min_file_size, max_file_size, files_num, base_dir, ovlfs_reg_dir, ovlfs_tuned_dir, seed_directories_batch, dirs_in_batch)
        else:
            seed_test_dirs(min_file_size, max_file_size, files_num, base_dir, ovlfs_reg_dir, ovlfs_tuned_dir)
        mount_filesystems(ovlfs_reg_dir, ovlfs_tuned_dir, metacopy, redirect_dir)    
        create_output_dirs(output_path)

    benchmark_functions = [cpp_update_time]

    for func in benchmark_functions:
        func(base_dir, Path(output_path) / func.__name__ / BASELINE_RESULT_FILE_NAME, runs_num=runs_num)
        func(Path(ovlfs_reg_dir) / OVLFS_MERGE_DIR, Path(output_path) / func.__name__/ REGULAR_OVLFS_RESULT_FILE_NAME, runs_num=runs_num)
        func(Path(ovlfs_tuned_dir) / OVLFS_MERGE_DIR, Path(output_path) / func.__name__ / TUNED_OVLFS_RESULT_FILE_NAME, runs_num=runs_num)
    plot_results(output_path)
    
    if unmount_ovlfs:
        unmount_filesystems(ovlfs_reg_dir, ovlfs_tuned_dir)
   
    if delete_files:
        delete_seeded_files(base_dir, ovlfs_reg_dir, ovlfs_tuned_dir)

if __name__ == '__main__':
    main()