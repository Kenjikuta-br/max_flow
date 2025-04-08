#pragma once

#include <vector>
#include <iostream>

// Represents a directed edge with a corresponding reverse edge in the residual graph
struct Edge {
    int to;       // Destination node
    int rev;      // Index of this edge's reverse edge in 'to' node's adjacency list
    int capacity; // Maximum capacity of the edge
    int flow;     // Current flow through the edge
};

class Graph {
public:
    Graph(int n = 0);

    // Adds a forward edge (with given capacity) and a reverse edge (with 0 capacity)
    void add_edge(int from, int to, int capacity);

    // Parses a graph from standard DIMACS max-flow format
    void read_dimacs(std::istream& in);

    // Returns the number of vertices in the graph
    int size() const;

    const std::vector<Edge>& adj(int u) const;

    // Used for updating flows directly during augmentation
    std::vector<std::vector<Edge>>& get_adj();

    const std::vector<Edge>& get_neighbors(int u) const;

    int get_source() const;
    int get_sink() const;

private:
    int n;                          // Number of vertices
    int source = -1, sink = -1;     // Indices of source and sink nodes
    std::vector<std::vector<Edge>> adj_list; // Adjacency list: each node has a list of outgoing edges
};
