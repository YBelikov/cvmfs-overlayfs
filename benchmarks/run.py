#!/usr/bin/env python

# Sole purpose of this script is to provide the single entry point for anyone who wants to run get plots without need to 
# launch each separate script separately
# Definetely, anyone can use scripts from this repo as standalone without running this script

import os
from optparse import OptionParser
from misc.log import *
from create_test_dir import produce_dir
from misc.copy_dir import copy_dir
from misc.utils import system
from plot_comparison import plot_results
from perform_benchmarks import benchmark_avg_chmod
from perform_benchmarks import OperationBenchmarkResult
from perform_benchmarks import output_result

OVLFS_LOWER_DIR='lower'
OVLFS_UPPER_DIR='upper'
OVLFS_MERGE_DIR='merge'
OVLFS_WORK_DIR='work'
BASE_BENCHMARK_RESULT_DIR='base_dir_results'
TUNED_OVLFS_RESULT_DIR='tuned_ovlfs_dir_results'
REGULAR_OVLFS_RESULT_DIR='regular_ovlfs_dir_results'

def seed_test_dirs(min_file_size, max_file_size, files_num, base_dir, ovlfs_reg_dir, ovlfs_tuned_dir):
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(ovlfs_reg_dir, exist_ok=True)
    os.makedirs(ovlfs_tuned_dir, exist_ok=True)
    for ovlfs_dir in [ovlfs_reg_dir, ovlfs_tuned_dir]:
        os.makedirs(os.path.join(ovlfs_dir, OVLFS_LOWER_DIR), exist_ok=True)
        os.makedirs(os.path.join(ovlfs_dir, OVLFS_UPPER_DIR), exist_ok=True)
        os.makedirs(os.path.join(ovlfs_dir, OVLFS_MERGE_DIR), exist_ok=True)
        os.makedirs(os.path.join(ovlfs_dir, OVLFS_WORK_DIR), exist_ok=True)
        
    produce_dir(base_dir, files_num, min_file_size, max_file_size)
    try:
        copy_dir(base_dir, os.path.join(ovlfs_reg_dir, OVLFS_LOWER_DIR))
        copy_dir(base_dir, os.path.join(ovlfs_tuned_dir, OVLFS_LOWER_DIR))
    except ValueError as ex:
        Logger.log(LogLevel.ERROR, f'Error on copying base directory contents: {ex}')

def mount_filesystems(ovlfs_reg_dir, ovlfs_tuned_dir):
    system(f'sudo mount -t overlay overlay -o lowerdir={os.path.join(ovlfs_tuned_dir, OVLFS_LOWER_DIR)},upperdir={os.path.join(ovlfs_tuned_dir, OVLFS_UPPER_DIR)},workdir={os.path.join(ovlfs_tuned_dir, OVLFS_WORK_DIR)},redirect_dir=on,metacopy=on {os.path.join(ovlfs_tuned_dir, OVLFS_MERGE_DIR)}')
    system(f'sudo mount -t overlay overlay -o lowerdir={os.path.join(ovlfs_reg_dir, OVLFS_LOWER_DIR)},upperdir={os.path.join(ovlfs_reg_dir, OVLFS_UPPER_DIR)},workdir={os.path.join(ovlfs_reg_dir, OVLFS_WORK_DIR)} {os.path.join(ovlfs_reg_dir, OVLFS_MERGE_DIR)}')

def unmount_filesystems(ovlfs_reg_dir, ovlfs_tuned_dir):
    system(f'sudo umount {os.path.join(ovlfs_reg_dir, OVLFS_MERGE_DIR)}')
    system(f'sudo umount {os.path.join(ovlfs_tuned_dir, OVLFS_MERGE_DIR)}')

def run_benchmark(target_dir, runs_num):
    return benchmark_avg_chmod(target_dir, runs_num)

def create_output_dirs(output_path):
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(os.path.join(output_path, BASE_BENCHMARK_RESULT_DIR), exist_ok=True)
    os.makedirs(os.path.join(output_path, TUNED_OVLFS_RESULT_DIR), exist_ok=True)
    os.makedirs(os.path.join(output_path, REGULAR_OVLFS_RESULT_DIR), exist_ok=True)


def main():
    usage = 'usage: <target path> [options]\n\
    This script plots a graph with benchmarking results acquired for baseline, overlayfs with features and regular overlayfs'
    parser = OptionParser(usage)
    parser.add_option('-l', '--min-file-size', dest='min_file_size', default=0, help='Min file size for random file contents in bytes')
    parser.add_option('-u', '--max-file-size', dest='max_file_size', default=10000000, help='Max file size for random file contents in bytes')
    parser.add_option('-n', '--number-of-files', dest='files_num', default=100, help='Number of files to generate')
    parser.add_option('-b', '--base-dir', dest='base_dir', default='~/base_dir', help='Path to the regular directory for baseline benchmark')
    parser.add_option('-r', '--overlay-fs-regular-dir', dest='ovlfs_reg_dir', default ='~/ovlfs_regular', help='Path to the directory where overlay FS structure without additional mount params will be spanned')
    parser.add_option('-f', '--overlay-fs-tuned-dir', dest='ovlfs_tuned_dir', default = '~/ovlfs_tuned', help='Path to directory where overlay FS structure with additional params will be spanned')
    parser.add_option('-t', '--runs_num', dest='runs_num', default = 100, help='Number of operation runs during benchmarking')
    parser.add_option('-o', '--output-path', dest='output_path', default = '~/ovlfs_benchmark_output', help='Path where files with benchmarking results are stored')
   
    (options, _) = parser.parse_args()
    
    try:
        min_file_size           = int(options.min_file_size)
        max_file_size           = int(options.max_file_size) 
        files_num               = int(options.files_num)
        base_dir                = str(options.base_dir)
        ovlfs_reg_dir           = str(options.ovlfs_reg_dir)
        ovlfs_tuned_dir         = str(options.ovlfs_tuned_dir)
        runs_num                = int(options.runs_num)
        output_path             = str(options.output_path)
    except ValueError:
        print('Cannot parse numerical options and/or parameters')
        exit(1)
    base_dir = os.path.expanduser(base_dir)
    ovlfs_reg_dir = os.path.expanduser(ovlfs_reg_dir)
    ovlfs_tuned_dir = os.path.expanduser(ovlfs_tuned_dir)
    output_path = os.path.expanduser(output_path)  
    
    seed_test_dirs(min_file_size, max_file_size, files_num, base_dir, ovlfs_reg_dir, ovlfs_tuned_dir)
    mount_filesystems(ovlfs_reg_dir, ovlfs_tuned_dir)
    base_dir_res = run_benchmark(base_dir, runs_num)

    ovlfs_tuned_res = run_benchmark(os.path.join(ovlfs_tuned_dir, OVLFS_MERGE_DIR), runs_num)
    ovlfs_reg_res = run_benchmark(os.path.join(ovlfs_reg_dir, OVLFS_MERGE_DIR), runs_num)
    create_output_dirs(output_path)
    baseline_result_dir = os.path.join(output_path, BASE_BENCHMARK_RESULT_DIR)
    ovlfs_tuned_result_dir = os.path.join(output_path, TUNED_OVLFS_RESULT_DIR)
    ovlfs_regular_result_dir = os.path.join(output_path, REGULAR_OVLFS_RESULT_DIR)
    output_result(baseline_result_dir, base_dir_res)
    output_result(ovlfs_tuned_result_dir, ovlfs_tuned_res)
    output_result(ovlfs_regular_result_dir, ovlfs_reg_res) 
    plot_results([baseline_result_dir, ovlfs_tuned_result_dir, ovlfs_regular_result_dir], ['baseline', 'ovlfs_tuned', 'ovlfs_regular'])
    #unmount_filesystems(ovlfs_reg_dir, ovlfs_tuned_dir)

if __name__ == '__main__':
    main()