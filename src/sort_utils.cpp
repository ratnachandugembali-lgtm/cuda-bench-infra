#include "sort_utils.h"
#include <algorithm>
#include <numeric>

void sort_ascending(std::vector<int>& data) {
    std::sort(data.begin(), data.end());
}

int sum_array(const std::vector<int>& data) {
    return std::accumulate(data.begin(), data.end(), 0);
}
