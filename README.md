# Ford-Fulkerson Family – Max Flow Algorithms

This repository contains an implementation of the **Ford-Fulkerson family of algorithms** for computing the **maximum s-t flow** in a flow network, along with multiple strategies to find augmenting paths.

## Implemented Strategies for Finding Augmenting Paths

- **Fattest Path (Widest Path)**: Chooses the path with the maximum bottleneck capacity.
- **Shortest Path (BFS-based)**: Uses Breadth-First Search to find the shortest augmenting path in terms of number of edges.
- **Randomized DFS**: Uses a randomized Depth-First Search to explore paths.

All strategies are modular and can be passed into the main Ford-Fulkerson function.

## Experimental Analysis

We analyze and compare the performance of each strategy by collecting:

- **Number of Iterations**: Number of augmenting paths found to reach the max flow.
- **Touched Elements**: Total number of vertices and edges visited.
- **Execution Time**: Measured in nanoseconds for higher precision.

These measurements are compared against the **RITT version** using Boost's Push-Relabel algorithm for benchmarking purposes.

## Usage

### Build the Project
```bash
make
```

### Compute Max Flow
Use the main binary to run max flow on a DIMACS-format graph using a chosen strategy:
```bash
./bin/max_flow bfs < graphs/mesh_graph.dimacs
./bin/max_flow dfs < graphs/mesh_graph.dimacs
./bin/max_flow fat < graphs/mesh_graph.dimacs
```

### Generate a Graph Using Professor's C Code
```bash
./bin/gengraph <function_id> <arg1> <arg2> <arg3> <output_file>
```
For example:
```bash
./bin/gengraph 1 50 50 37 > graphs/mesh_graph.dimacs
```

### Run the RITT Version (Boost Push-Relabel)
```bash
./bin/ritt_max_flow < graphs/mesh_graph.dimacs
```

### Benchmark All Implementations
Run all algorithms (bfs, dfs, fat, ritt) on every `.dimacs` file in the graphs folder:
```bash
./scripts/benchmark.sh
```
This creates a CSV file `results.csv` with:
```
graph,strategy,max_flow,time_ns
```

## Project Structure
```
.
├── include/                      # Header files
│   ├── graph.hpp                 # Graph representation
│   ├── ford_fulkerson.hpp       # Max-flow algorithm header
│   └── find_path_headers/       # Headers for path finding strategies
│       ├── bfs.hpp
│       ├── dfs_random.hpp
│       ├── fattest_path.hpp
├── src/                          # Source code
│   ├── main.cpp                  # Entry point
│   ├── graph.cpp
│   ├── ford_fulkerson.cpp
│   ├── find_path_sources/       # Path strategy implementations
│   │   ├── bfs.cpp
│   │   ├── dfs_random.cpp
│   │   └── fattest_path.cpp
│   └── support_code_ritt/       # Professor-provided code
│       ├── new_washington.c     # Graph generator
│       └── maxflow.cpp          # RITT's max-flow implementation using Boost
├── bin/                          # Compiled executables
├── obj/                          # Intermediate object files
├── graphs/                       # Folder to store or generate .dimacs files
├── results.csv                   # Output file with benchmark results
├── Makefile                      # Makefile to build everything
└── bash/
    └── test_correctness.sh             # Automation for testing and benchmarking
```

## Notes
- The project uses a `visitedToken` optimization to reduce memory operations when tracking visited nodes.
- Execution times are measured using `date +%s.%N` to ensure nanosecond resolution.
- All augmenting strategies are interchangeable thanks to the `PathFindingStrategy` function pointer abstraction.

## Author
Gabriel Kenji Yatsuda Ikuta (based on guidance and infrastructure from Prof. Marcus Ritt)

---

### 📚 References

- [William Fiset’s Network Flow Algorithms (GitHub)](https://github.com/williamfiset/Algorithms/tree/master/src/main/java/com/williamfiset/algorithms/graphtheory/networkflow)
- [Max Flow Algorithm Lecture (YouTube)](https://www.youtube.com/watch?v=Xu8jjJnwvxE&list=PLDV1Zeh2NRsDj3NzHbbFIC58etjZhiGcG&index=2&ab_channel=WilliamFiset)
