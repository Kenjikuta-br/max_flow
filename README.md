# Ford-Fulkerson Family – Max Flow Algorithms

This repository contains an implementation of the **Ford-Fulkerson family of algorithms** for computing the **maximum s-t flow** in a flow network.

## Implemented Strategies for Finding Augmenting Paths

- **Fattest Path (Widest Path)**: Chooses the path with the maximum bottleneck capacity.
- **Shortest Path (BFS-based)**: Uses Breadth-First Search to find the shortest augmenting path in terms of number of edges.
- **Randomized DFS**: Uses a randomized Depth-First Search to explore paths.

## Experimental Analysis

We analyze the performance of the algorithms based on:

- **Number of Iterations**: Total number of augmenting paths used to reach the max flow.
- **Number of Operations**: Total number of vertices and edges *touched* during execution.

We also compare the **empirical deficiency of iterations** and the **cost per iteration** with the **theoretical worst-case complexity** of each strategy.

## Goals

- Understand and compare the practical performance of different Ford-Fulkerson variants.
- Provide insights into how path selection strategies affect efficiency.
- Explore the trade-offs between simplicity, speed, and worst-case behavior.

## Usage

Coming soon: example usage and benchmarks.
