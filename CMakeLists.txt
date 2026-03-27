cmake_minimum_required(VERSION 3.20)

project(cuda_bench_infra CXX)

set(CMAKE_CXX_STANDARD 17)

include_directories(include)

add_library(sort_utils src/sort_utils.cpp)

add_subdirectory(benchmarks)
