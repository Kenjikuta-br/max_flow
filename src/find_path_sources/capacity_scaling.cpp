#include "find_path_headers/capacity_scaling.hpp"
#include <queue>
#include <stack>
#include <limits>
#include <algorithm>
#include <cmath>

namespace {
    std::vector<uint64_t> visited;
    uint64_t visitedToken = 1;

    void reset(size_t n) {
        if (visited.size() < n) visited.assign(n, 0);
        visitedToken++;
    }
}

// Internal function to find a path with minimum capacity threshold 'delta'
static bool dfs_with_delta(const Graph& graph, int s, int t, Path& path, int delta) {
    int n = graph.size();
    std::vector<std::pair<int, int>> parent(n, {-1, -1});
    std::stack<int> st;
    st.push(s);
    visited[s] = visitedToken;

    while (!st.empty()) {
        int u = st.top();
        st.pop();

        const auto& neighbors = graph.get_neighbors(u);
        for (size_t i = 0; i < neighbors.size(); ++i) {
            const Edge& e = neighbors[i];
            int residual = e.remaining_capacity();
            if (residual >= delta && visited[e.to] != visitedToken) {
                visited[e.to] = visitedToken;
                parent[e.to] = {u, static_cast<int>(i)};
                st.push(e.to);
                if (e.to == t) break;
            }
        }
    }

    if (visited[t] != visitedToken) return false;

    // Reconstruct path
    path.clear();
    for (int u = t; u != s; u = parent[u].first) {
        int prev = parent[u].first;
        int idx = parent[u].second;
        path.push_back({prev, idx});
    }
    std::reverse(path.begin(), path.end());
    return true;
}

bool capacity_scaling_path(const Graph& graph, int s, int t, Path& path) {
    int max_cap = 0;

    // Find the maximum edge capacity in the graph
    for (int u = 0; u < graph.size(); ++u) {
        for (const Edge& e : graph.get_neighbors(u)) {
            max_cap = std::max(max_cap, e.remaining_capacity());
        }
    }

    // Start with the highest power of 2 <= max_cap
    int delta = 1;
    while (delta <= max_cap) delta <<= 1;
    delta >>= 1;

    // Try to find a path for the current delta threshold
    while (delta > 0) {
        reset(graph.size());
        if (dfs_with_delta(graph, s, t, path, delta)) return true;
        delta >>= 1; // Reduce delta if no path is found at this threshold
    }

    return false;
}
