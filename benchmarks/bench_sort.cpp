#include <benchmark/benchmark.h>
#include "sort_utils.h"
#include <vector>
#include <random>

static void BM_SortAscending(benchmark::State& state) {
    int n = state.range(0);

    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(0, 100000);

    for (auto _ : state) {
        std::vector<int> data(n);
        for (auto& x : data) x = dist(rng);
        sort_ascending(data);
    }

    state.SetItemsProcessed(state.iterations() * n);
}

static void BM_SumArray(benchmark::State& state) {
    int n = state.range(0);
    std::vector<int> data(n, 1);

    for (auto _ : state) {
        benchmark::DoNotOptimize(sum_array(data));
    }

    state.SetItemsProcessed(state.iterations() * n);
}

BENCHMARK(BM_SortAscending)->Arg(1000)->Arg(10000)->Arg(100000);
BENCHMARK(BM_SumArray)->Arg(1000)->Arg(10000)->Arg(100000);

BENCHMARK_MAIN();
