find_package(benchmark REQUIRED)

add_executable(bench_sort bench_sort.cpp)

target_link_libraries(bench_sort sort_utils benchmark::benchmark)
