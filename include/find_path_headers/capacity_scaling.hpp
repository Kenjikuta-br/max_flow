#pragma once

#include "graph.hpp"
#include <vector>

// Path format: (from_node, edge_index)
using Path = std::vector<std::pair<int, int>>;

// Global visited token state reused between calls
namespace scaling_state {
    std::vector<uint64_t> visited;
    uint64_t visitedToken = 1;

    // Resets state for a new search round
    void reset(size_t n) {
        if (visited.size() < n) visited.assign(n, 0);
        visitedToken++;
    }
}

/**
 * Finds an s-t augmenting path using capacity scaling DFS.
 * Only explores edges with residual capacity >= current delta threshold.
 * Compatible with Ford-Fulkerson signature.
 */
bool capacity_scaling_path(const Graph& graph, int s, int t, Path& path);
