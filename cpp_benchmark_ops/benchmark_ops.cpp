#include <fstream>
#include <map>
#include <filesystem>
#include <iostream>
#include <chrono>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include "scope_exit.h"

using benchmark_map = std::map<uintmax_t, uint64_t>;

void updateAccessTime(benchmark_map& benchmarkingResults, const std::filesystem::path& targetDir)
{
    if (!std::filesystem::is_directory(targetDir))
    {
        throw std::logic_error("Non directory provided!");
    }

    int dirfd = open(targetDir.c_str(), O_RDONLY | O_DIRECTORY);

    SCOPE_EXIT { close(dirfd); };

    if (dirfd == -1)
    {
        perror("Dir open");
        throw std::domain_error("Unable to open target directory in readonly mode");
    }

    for (const auto& entry : std::filesystem::directory_iterator(targetDir))
    {
        if (!entry.is_regular_file())
        {   
            std::cout << entry.path();
            continue;
        }
       
        timespec tspec[2];
        tspec[0].tv_nsec = UTIME_NOW;
        tspec[1].tv_nsec = UTIME_NOW;
        auto start = std::chrono::high_resolution_clock::now();
        utimensat(dirfd, entry.path().c_str(), tspec, 0);
        auto end = std::chrono::high_resolution_clock::now();
        auto elapsedTime = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);
        uintmax_t entrySize = entry.file_size();
        if (benchmarkingResults.find(entrySize) == benchmarkingResults.end())
        {
            benchmarkingResults[entry.file_size()] = elapsedTime.count();
        }
        else 
        {
            benchmarkingResults[entry.file_size()] += elapsedTime.count();
        }
    }
}

void changeMode(benchmark_map& benchmarkingResults, const std::filesystem::path& targetDir) 
{
    if (!std::filesystem::is_directory(targetDir))
    {
        throw std::logic_error("Non directory provided!");
    }

    for (const auto& entry : std::filesystem::directory_iterator(targetDir))
    {
        if (!entry.is_regular_file())
        {   
            std::cout << entry.path();
            continue;
        }
        auto start = std::chrono::high_resolution_clock::now();
        chmod(entry.path().c_str(), S_IRWXU | S_IRWXG | S_IRWXO);
        auto end = std::chrono::high_resolution_clock::now();
        auto elapsedTime = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);
        uintmax_t entrySize = entry.file_size();
        if (benchmarkingResults.find(entrySize) == benchmarkingResults.end())
        {
            benchmarkingResults[entry.file_size()] = elapsedTime.count();
        }
        else 
        {
            benchmarkingResults[entry.file_size()] += elapsedTime.count();
        }
    }
}

void writeOutput(std::ofstream& outputStream, const benchmark_map& benchmarkingResults)
{
    for (const auto& dictPair : benchmarkingResults)
    {
        outputStream << dictPair.first << ' ' << dictPair.second * 1e-6 << '\n';   
    }
}

int main(int argc, char** argv)
{ 
    int numberOfRuns = std::stoi(argv[1]);
    std::filesystem::path inputDir = argv[2];
    std::filesystem::path outputFile = argv[3];

    std::filesystem::path outputDir = outputFile.parent_path();
    if (!std::filesystem::exists(outputDir))
    {
        std::filesystem::create_directory(outputDir);
    }
    benchmark_map benchmarkingResults;
    for (int i = 0; i < numberOfRuns; ++i)
    {
        updateAccessTime(benchmarkingResults, inputDir);
    }
    std::ofstream output(outputFile);
    writeOutput(output, benchmarkingResults);
    return 0;
}