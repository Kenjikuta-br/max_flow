#include "find_path_headers/bfs.hpp"
#include <queue>
#include <algorithm>

bool bfs_path(const Graph& graph, int s, int t, Path& path) {
    int n = graph.size();
    std::vector<bool> visited(n, false);
    std::vector<std::pair<int, int>> parent(n, {-1, -1}); // {prev_node, edge_index}

    std::queue<int> q;
    q.push(s);
    visited[s] = true;

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        const auto& neighbors = graph.get_neighbors(u);  // AQUI!

        for (size_t i = 0; i < neighbors.size(); ++i) {
            const Edge& e = neighbors[i];
            if (!visited[e.to] && e.capacity > e.flow) {
                visited[e.to] = true;
                parent[e.to] = {u, i};
                q.push(e.to);
                if (e.to == t) break;
            }
        }
    }
    

    // No path to sink
    if (!visited[t]) return false;

    // Reconstruct path from t to s
    path.clear();
    for (int u = t; u != s; u = parent[u].first) {
        int prev = parent[u].first;
        int idx = parent[u].second;
        path.push_back({prev, idx});
    }

    std::reverse(path.begin(), path.end()); // Make path go from s to t
    return true;
}
