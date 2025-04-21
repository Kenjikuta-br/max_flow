#include "ford_furkenson.hpp"
#include <algorithm>
#include <climits>

// Augments the flow along a valid s-t path.
// Returns how much flow was added (bottleneck capacity).
int augment(Graph& graph, const Path& path) {
    int bottleneck = INT_MAX;
    auto& adj = graph.get_adj(); // Reference to adjacency list for flow updates

    // Find the bottleneck: minimum residual capacity in the path
    for (const auto& [u, idx] : path) {
        const Edge& e = adj[u][idx];
        bottleneck = std::min(bottleneck, e.remaining_capacity()); // using method
    }

    // Apply the bottleneck flow to the path
    for (const auto& [u, idx] : path) {
        Edge& e = adj[u][idx];
        Edge& rev = adj[e.to][e.rev];
        e.augment(bottleneck, rev); // using method
    }

    return bottleneck;
}

// Repeatedly finds augmenting paths and applies flow until none remain
int ford_fulkerson(Graph& graph, int s, int t, PathFindingStrategy find_path) {
    int max_flow = 0;
    Path path;

    // Main loop: search-augment-repeat
    while (find_path(graph, s, t, path)) {
        int added_flow = augment(graph, path);
        max_flow += added_flow;
    }

    //graph.print_residual_graph();

    return max_flow;
}
