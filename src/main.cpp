#include "graph.hpp"
#include "ford_furkenson.hpp"
#include "find_path_headers/bfs.hpp"
#include "find_path_headers/dfs_random.hpp"
#include "find_path_headers/fattest.hpp"


#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Uso: " << argv[0] << " bfs|dfs|fat|scaling|dinics < dimacs_graph\n";
        return 1;
    }

    std::string strategy_name = argv[1];
    PathFindingStrategy strategy = nullptr;

    if (strategy_name == "bfs") {
        strategy = bfs_path;
    } else if (strategy_name == "dfs") {
        strategy = dfs_path;
    } else if (strategy_name == "fat") {
        strategy = fattest_path;
    } else if (strategy_name == "scaling") {
        //strategy = capacity_scaling_path;
        std::cerr << "Ainda não implementado capacity scaling\n";
    } else if (strategy_name == "dinics") {
        //strategy = dinics_path;
        std::cerr << "Ainda não implementado dinics\n";
    } else {
        std::cerr << "Estrategia inválida: " << strategy_name << ". Use bfs ou dfs.\n";
        return 1;
    }

    Graph graph;
    graph.read_dimacs(std::cin);

    int source = graph.get_source();
    int sink = graph.get_sink();

    int max_flow = ford_fulkerson(graph, source, sink, strategy);
    std::cout << max_flow << "\n";

    return 0;
}