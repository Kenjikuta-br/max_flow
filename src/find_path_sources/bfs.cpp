#include "find_path_headers/bfs.hpp"
#include <queue>
#include <algorithm>

bool bfs_path(const Graph& graph, int s, int t, Path& path) {
    int n = graph.size();
    bfs_state::reset(n);  // Prepare visited array and increment token

    std::vector<std::pair<int, int>> parent(n, {-1, -1}); // Stores how each node was reached

    std::queue<int> q;
    q.push(s);
    bfs_state::visited[s] = bfs_state::visitedToken; // Mark source as visited for this iteration

    // Standard BFS loop to find an s-t path with positive residual capacity
    while (!q.empty()) {
        int u = q.front();
        q.pop();

        const auto& neighbors = graph.get_neighbors(u);

        for (size_t i = 0; i < neighbors.size(); ++i) {
            const Edge& e = neighbors[i];

            // Skip visited nodes or saturated edges
            if (bfs_state::visited[e.to] != bfs_state::visitedToken && e.capacity > e.flow) {
                bfs_state::visited[e.to] = bfs_state::visitedToken;
                parent[e.to] = {u, static_cast<int>(i)};
                q.push(e.to);
                if (e.to == t) break; // Early stop if sink is reached
            }
        }
    }

    // Sink wasn't reached => no augmenting path
    if (bfs_state::visited[t] != bfs_state::visitedToken) return false;

    // Reconstruct path from t to s using parent info
    path.clear();
    for (int u = t; u != s; u = parent[u].first) {
        int prev = parent[u].first;
        int idx = parent[u].second;
        path.push_back({prev, idx});
    }

    std::reverse(path.begin(), path.end()); // Ensure path goes from s to t
    return true;
}
