# Cheat Sheet Handy Commands

The main executable uses a DIMACS input file to compute the maximum flow using the chosen path-finding strategy. For example, if you want to use BFS, run:

``` bash
./bin/max_flow bfs < graphs/mesh_graph.dimacs
```

To generate a graph using the provided new_washington.c code, run:
``` bash
./bin/gengraph  function arg1 arg2 arg3 <output_file>
```
Mesh = 1, Rows = 50, Columns = 50, Max capacity = 37, output_file = mesh_graph
For example:
``` bash
./bin/gengraph 1 50 50 37 graphs/mesh_graph.dimacs
```

To run the RITT version of the maximum flow program, execute:
``` bash
./bin/ritt_max_flow < graphs/mesh_graph.dimacs
```







# Project Structure

```
.
├── include/              # Header files for the project (e.g., graph.hpp, ford_fulkerson.hpp, strategies/)
├── src/                  # Source files
│   ├── main.cpp          # Main function (entry point)
│   ├── graph.cpp         # Graph representation and DIMACS input parsing
│   ├── ford_fulkerson.cpp# Ford-Fulkerson implementation
│   ├── find_path_sources/
│   │    └── bfs.cpp      # BFS strategy for finding augmenting paths
│   └── support_code_ritt/
│        ├── new_washington.c   # Graph generator in C (provided by your professor)
│        └── maxflow.cpp         # RITT version implementation for maximum flow
├── bin/                  # Folder where executables will be placed (created during build)
├── obj/                  # Object files directory (created during build)
└── Makefile              # Makefile to compile the project
```