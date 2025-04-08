#include "find_path_headers/dfs_random.hpp"
#include "find_path_headers/bfs.hpp" // for bfs_state
#include <vector>
#include <algorithm>
#include <random>
#include <stack>

bool dfs_path(const Graph& graph, int source, int sink, Path& path) {
    int n = graph.size();
    bfs_state::reset(n);  // resets visitedToken and resizes visited

    std::vector<std::pair<int, int>> parent(n, {-1, -1}); // {prev_node, edge_index}
    std::stack<int> s;
    s.push(source);
    bfs_state::visited[source] = bfs_state::visitedToken;

    std::random_device rd;
    std::mt19937 rng(rd());

    while (!s.empty()) {
        int u = s.top();
        s.pop();

        const auto& neighbors = graph.get_neighbors(u);

        // Generate a shuffled list of edge indices for randomized traversal
        std::vector<int> indices(neighbors.size());
        for (size_t i = 0; i < neighbors.size(); ++i) indices[i] = static_cast<int>(i);
        std::shuffle(indices.begin(), indices.end(), rng);

        for (int i : indices) {
            const Edge& e = neighbors[i];
            if (bfs_state::visited[e.to] != bfs_state::visitedToken && e.remaining_capacity() > 0) {
                bfs_state::visited[e.to] = bfs_state::visitedToken;
                parent[e.to] = {u, i};
                s.push(e.to);
                if (e.to == sink) break;
            }
        }
    }

    if (bfs_state::visited[sink] != bfs_state::visitedToken) return false;

    // Reconstruct path from sink to source
    path.clear();
    for (int u = sink; u != source; u = parent[u].first) {
        int prev = parent[u].first;
        int idx = parent[u].second;
        path.push_back({prev, idx});
    }

    std::reverse(path.begin(), path.end());
    return true;
}
