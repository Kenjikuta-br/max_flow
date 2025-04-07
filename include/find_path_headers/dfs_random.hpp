#pragma once

#include "graph.hpp"
#include <vector>
#include <utility>

// Type alias used across the project for clarity
using Path = std::vector<std::pair<int, int>>;

/**
 * @brief Randomized DFS to find an augmenting path in residual graph.
 * 
 * The traversal is randomized by shuffling adjacency lists before exploring.
 * The path is returned in the format of (previous_node, edge_index) pairs.
 * 
 * @param graph Residual graph.
 * @param source Source node.
 * @param sink Sink node.
 * @param path Stores the resulting augmenting path.
 * @return True if path is found, false otherwise.
 */
bool dfs_path(const Graph& graph, int source, int sink, Path& path);
