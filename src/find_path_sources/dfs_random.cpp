#include "find_path_headers/dfs_random.hpp"
#include <vector>
#include <algorithm>
#include <random>
#include <stack>

bool dfs_path(const Graph& graph, int source, int sink, Path& path) {
    int n = graph.size();
    std::vector<bool> visited(n, false);
    std::vector<std::pair<int, int>> parent(n, {-1, -1}); // {prev_node, edge_index}
    std::stack<int> s;

    s.push(source);
    visited[source] = true;

    std::random_device rd;
    std::mt19937 rng(rd()); // Mersenne Twister RNG

    while (!s.empty()) {
        int u = s.top();
        s.pop();

        auto neighbors = graph.get_neighbors(u);
        std::vector<int> indices(neighbors.size());
        for (size_t i = 0; i < neighbors.size(); ++i) indices[i] = i;
        std::shuffle(indices.begin(), indices.end(), rng);

        for (size_t i : indices) {
            const Edge& e = neighbors[i];
            if (!visited[e.to] && e.capacity > e.flow) {
                visited[e.to] = true;
                parent[e.to] = {u, i};
                s.push(e.to);
                if (e.to == sink) break;
            }
        }
    }

    // No path found
    if (!visited[sink]) return false;

    // Reconstruct the path from sink to source
    path.clear();
    for (int u = sink; u != source; u = parent[u].first) {
        int prev = parent[u].first;
        int idx = parent[u].second;
        path.push_back({prev, idx});
    }

    std::reverse(path.begin(), path.end()); // Make path go from source to sink
    return true;
}
