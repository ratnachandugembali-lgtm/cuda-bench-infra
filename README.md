# cuda-bench-infra

A lightweight C++ benchmarking scaffold for microbenchmarks.

This project currently includes:

- A reusable utility library in [`include/sort_utils.h`](include/sort_utils.h) and [`src/sort_utils.cpp`](src/sort_utils.cpp)
- Google Benchmark-based performance tests in [`benchmarks/bench_sort.cpp`](benchmarks/bench_sort.cpp)
- A CMake build setup at the repository root and in [`benchmarks/CMakeLists.txt`](benchmarks/CMakeLists.txt)

## What It Benchmarks

- `BM_SortAscending`: sorts randomly generated integer arrays
- `BM_SumArray`: computes the sum of integer arrays

Both benchmarks run at multiple input sizes (`1,000`, `10,000`, `100,000`) to compare scaling behavior.

## Requirements

- CMake 3.20+
- C++17 compiler
- [Google Benchmark](https://github.com/google/benchmark) installed and discoverable by CMake

## Build

```bash
cmake -S . -B build
cmake --build build
```

## Run Benchmarks

```bash
./build/benchmarks/bench_sort
```

## Project Layout

```text
.
├── CMakeLists.txt
├── include/
│   └── sort_utils.h
├── src/
│   └── sort_utils.cpp
└── benchmarks/
    ├── CMakeLists.txt
    └── bench_sort.cpp
```
