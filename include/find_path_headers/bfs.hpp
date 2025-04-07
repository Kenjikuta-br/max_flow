#pragma once
#include "graph.hpp"
#include <vector>


using Path = std::vector<std::pair<int, int>>;
// Finds an s-t path using BFS and stores it in `path`.
// Returns true if a path is found, false otherwise.
bool bfs_path(const Graph& graph, int s, int t, Path& path);

