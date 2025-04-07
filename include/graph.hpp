#pragma once

#include <vector>
#include <iostream>

struct Edge {
    int to;
    int rev; // Index of the reverse edge in the adjacency list
    int capacity;
    int flow;
};

class Graph {
public:
    Graph(int n = 0);

    void add_edge(int from, int to, int capacity);
    void read_dimacs(std::istream& in);

    int size() const;
    const std::vector<Edge>& adj(int u) const;
    std::vector<std::vector<Edge>>& get_adj();
    const std::vector<Edge>& get_neighbors(int u) const;

    int get_source() const;
    int get_sink() const;

private:
    int n;
    int source = -1;
    int sink = -1;
    std::vector<std::vector<Edge>> adj_list;
};
