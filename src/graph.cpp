// graph.cpp
#include "graph.hpp"
#include <sstream>
#include <stdexcept>

// Constructor that initializes the graph with n nodes
Graph::Graph(int n) : n(n), adj_list(n) {}

// Adds a forward and reverse edge (for residual graph) between 'from' and 'to'
void Graph::add_edge(int from, int to, int capacity) {
   // Forward edge: from → to with given capacity
    Edge forward = {to, from, static_cast<int>(adj_list[to].size()), capacity, 0};
    // Reverse edge: to → from with 0 capacity (initially), used for flow cancellation
    Edge backward = {from, to, static_cast<int>(adj_list[from].size()), 0, 0};

    adj_list[from].push_back(forward);
    adj_list[to].push_back(backward);
}

int Graph::size() const {
    return n;
}

// Returns the adjacency list of a given node
const std::vector<Edge>& Graph::adj(int u) const {
    return adj_list[u];
}

// Returns the list of edges from node u (same as adj)
const std::vector<Edge>& Graph::get_neighbors(int u) const {
    return adj_list[u];
}

// Returns the full adjacency list for modifying flows
std::vector<std::vector<Edge>>& Graph::get_adj() {
    return adj_list;
}

int Graph::get_source() const {
    return source;
}

int Graph::get_sink() const {
    return sink;
}

// Reads a graph in DIMACS max-flow format from an input stream
void Graph::read_dimacs(std::istream& in) {
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty() || line[0] == 'c') continue; // Skip comments

        std::istringstream iss(line);
        char type;
        iss >> type;

        if (type == 'p') {
            std::string problem_type;
            int nodes, arcs;
            iss >> problem_type >> nodes >> arcs;
            if (problem_type != "max") {
                throw std::runtime_error("Only 'max' problems are supported");
            }
            n = nodes;
            adj_list.assign(n, {});
        } else if (type == 'n') {
            int id;
            char role;
            iss >> id >> role;
            if (role == 's') source = id - 1;
            if (role == 't') sink = id - 1;
        } else if (type == 'a') {
            int from, to, cap;
            iss >> from >> to >> cap;
            add_edge(from - 1, to - 1, cap);
        }
    }

    if (source == -1 || sink == -1) {
        throw std::runtime_error("Source or sink node not defined");
    }
}
