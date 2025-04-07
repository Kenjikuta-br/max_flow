#pragma once
#include "graph.hpp"
#include <functional>
#include <vector>

// Each pair represents an edge used in the path: (from_node, index of edge in graph[from_node])
using Path = std::vector<std::pair<int, int>>;


// Type for a path-finding strategy function
using PathFindingStrategy = std::function<bool(const Graph&, int s, int t, Path& path)>;

// Runs Ford-Fulkerson algorithm using a given strategy.
// Returns the maximum flow value and optionally stores flow path stats.
int ford_fulkerson(Graph& graph, int s, int t, PathFindingStrategy find_path);
