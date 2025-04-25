#include "find_path_headers/dfs_random.hpp"
#include "find_path_headers/bfs.hpp" // for bfs_state
#include <vector>
#include <algorithm>
#include <random>
#include <stack>

bool dfs_path(const Graph& graph, int source, int sink, Path& path, FFStats* stats) {
    int n = graph.size();
    bfs_state::reset(n);  // resets visitedToken and resizes visited

    std::vector<std::pair<int, int>> parent(n, {-1, -1}); // {prev_node, edge_index}
    std::stack<int> s;
    s.push(source);
    bfs_state::visited[source] = bfs_state::visitedToken;

    std::random_device rd;
    std::mt19937 rng(rd());

    // Counters for statistics
    int visited_nodes = 1; // source is initially visited
    int visited_arcs_residual = 0;
    int visited_arcs_forward =0;

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
            if (e.remaining_capacity() > 0) {
                if(e.capacity > 0){
                    ++visited_arcs_forward;
                }

                ++visited_arcs_residual; // count arc only if it has remaining capacity
    
                if (bfs_state::visited[e.to] != bfs_state::visitedToken) {
                    bfs_state::visited[e.to] = bfs_state::visitedToken;
                    parent[e.to] = {u, i};
                    s.push(e.to);
                    ++visited_nodes; // count only when visiting a new node
    
                    if (e.to == sink) break;
                }
            }
        }
    }

    stats->visited_nodes_per_iter.push_back(visited_nodes);
    stats->visited_forward_arcs_per_iter.push_back(visited_arcs_forward);
    stats->visited_residual_arcs_per_iter.push_back(visited_arcs_residual);

    if (bfs_state::visited[sink] != bfs_state::visitedToken) {
        return false;
    }
   

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
