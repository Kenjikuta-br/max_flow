// graph.cpp
#include "graph.hpp"
#include <sstream>
#include <stdexcept>

Graph::Graph(int n) : n(n), adj_list(n) {}

void Graph::add_edge(int from, int to, int capacity) {
    Edge forward = {to, static_cast<int>(adj_list[to].size()), capacity, 0};
    Edge backward = {from, static_cast<int>(adj_list[from].size()), 0, 0};

    adj_list[from].push_back(forward);
    adj_list[to].push_back(backward);
}

int Graph::size() const {
    return n;
}

const std::vector<Edge>& Graph::adj(int u) const {
    return adj_list[u];
}

const std::vector<Edge>& Graph::get_neighbors(int u) const{
    return adj_list[u];
}

std::vector<std::vector<Edge>>& Graph::get_adj() {
    return adj_list;
}

int Graph::get_source() const {
    return source;
}

int Graph::get_sink() const {
    return sink;
}

void Graph::read_dimacs(std::istream& in) {
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty() || line[0] == 'c') continue;

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
