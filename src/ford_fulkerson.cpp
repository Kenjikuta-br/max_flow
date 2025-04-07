#include "ford_furkenson.hpp"
#include <algorithm>
#include <climits>


// Tries to augment the flow along a given path.
// Returns how much flow was added.
int augment(Graph& graph, const Path& path) {
    int bottleneck = INT_MAX;
    auto& adj = graph.get_adj();  // pegar referência à lista de adjacência

    for (const auto& [u, idx] : path) {
        const Edge& e = adj[u][idx];
        bottleneck = std::min(bottleneck, e.capacity - e.flow);
    }

    for (const auto& [u, idx] : path) {
        Edge& e = adj[u][idx];
        Edge& rev = adj[e.to][e.rev];

        e.flow += bottleneck;
        rev.flow -= bottleneck;
    }

    return bottleneck;
}


int ford_fulkerson(Graph& graph, int s, int t, PathFindingStrategy find_path) {
    int max_flow = 0;
    Path path;

    // Keep finding augmenting paths using the selected strategy
    while (find_path(graph, s, t, path)) {
        int added_flow = augment(graph, path);
        max_flow += added_flow;
    }

    return max_flow;
}
