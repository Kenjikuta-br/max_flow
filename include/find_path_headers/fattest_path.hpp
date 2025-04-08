#pragma once
#include "graph.hpp"
#include <vector>

// Path type alias: (from, edge index)
using Path = std::vector<std::pair<int, int>>;

/**
 * @brief Finds the fattest (widest bottleneck capacity) augmenting path from source to sink.
 * 
 * @param graph The residual graph.
 * @param s The source node.
 * @param t The sink node.
 * @param path The resulting path if found.
 * @return true if a path is found, false otherwise.
 */
bool fattest_path(const Graph& graph, int s, int t, Path& path);
