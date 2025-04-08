#include "find_path_headers/fattest_path.hpp"
#include <vector>
#include <queue>
#include <limits>
#include <algorithm>

// Represents a node in the priority queue with its bottleneck capacity
struct State {
    int cap;
    int node;
    bool operator<(const State& other) const {
        return cap < other.cap; // for max-heap behavior
    }
};

bool fattest_path(const Graph& graph, int s, int t, Path& path) {
    int n = graph.size();
    int INF = std::numeric_limits<int>::max();

    std::vector<int> max_cap(n, 0); // max bottleneck capacity to each node
    std::vector<std::pair<int, int>> parent(n, {-1, -1}); // to reconstruct the path

    std::priority_queue<State> pq;
    pq.push({INF, s}); // start from source with infinite capacity
    max_cap[s] = INF;

    // Modified Dijkstra: prioritize paths with highest bottleneck capacity
    while (!pq.empty()) {
        State state = pq.top();
        pq.pop();
        int u = state.node;

        const auto& neighbors = graph.get_neighbors(u);
        for (size_t i = 0; i < neighbors.size(); ++i) {
            const Edge& e = neighbors[i];
            int residual = e.capacity - e.flow;
            if (residual <= 0) continue; // skip saturated edges

            // Bottleneck capacity of current path
            int cap = std::min(max_cap[u], residual);
            // If we found a better path to e.to, update it
            if (cap > max_cap[e.to]) {
                max_cap[e.to] = cap;
                parent[e.to] = {u, static_cast<int>(i)};
                pq.push({cap, e.to});
            }
        }
    }

    if (max_cap[t] == 0) return false; // No path found

    // Reconstruct the path from sink to source using parent[]
    path.clear();
    for (int u = t; u != s; u = parent[u].first) {
        int prev = parent[u].first;
        int idx = parent[u].second;
        path.push_back({prev, idx});
    }

    std::reverse(path.begin(), path.end()); // path is constructed backward, so reverse
    return true;
}
