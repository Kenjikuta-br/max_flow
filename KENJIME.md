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


# 🧠 Max Flow Algorithms Overview

## ✅ Summary Table

| Algorithm           | Time Complexity         | Key Strength                 | Key Weakness                   |
|---------------------|-------------------------|-------------------------------|--------------------------------|
| **BFS (Edmonds-Karp)** | O(V × E²)              | Simple, finds shortest path   | Slow on large graphs           |
| **Random DFS**         | O(E × max_flow)        | Simple to implement           | Can be exponential             |
| **Fattest Path**       | O(E log V × max_flow)  | Pushes more flow per step     | Heavier per-iteration cost     |
| **Capacity Scaling**   | O(E² log C)            | Efficient with big capacities | More complex than basic BFS    |
| **Dinic’s**            | O(V² × E)              | Excellent theoretical bounds  | Complex implementation         |

---

## 🔍 1. BFS (Edmonds-Karp)

### **What it does & how**
- Uses **Breadth-First Search** to find the **shortest augmenting path** (by number of edges) in the residual graph.
- Augments flow along that path until no such path exists.

### **Complexity**
- **O(V × E²)**

### ✅ Pros
- Simple and intuitive.
- Guarantees polynomial runtime.

### ❌ Cons
- Can be slow for graphs with many edges or high max flow.

### 💪 Strength
- Finds shortest paths in terms of edges.

### 🧱 Weakness
- Inefficient for large graphs with large capacities.

---

## 🔍 2. Random DFS (Classic Ford-Fulkerson)

### **What it does & how**
- Uses **Depth-First Search** (often randomized) to find any augmenting path.
- Continues until no more such paths are available.

### **Complexity**
- **O(E × max_flow)** — Can be **exponential** if capacities are irrational.

### ✅ Pros
- Very easy to implement.
- Works well in practice on small graphs.

### ❌ Cons
- May loop forever with irrational capacities.
- Inefficient in worst case.

### 💪 Strength
- Lightweight and flexible.

### 🧱 Weakness
- Bad worst-case behavior.

---

## 🔍 3. Fattest Path

### **What it does & how**
- Always chooses a path with the **largest bottleneck capacity** (minimum edge capacity on path is maximized).
- Can be found using a **modified Dijkstra** algorithm.

### **Complexity**
- **O(E log V × max_flow)**

### ✅ Pros
- Pushes larger flows in fewer iterations.
- Efficient in sparse graphs with large capacities.

### ❌ Cons
- More complex per iteration.
- Needs priority queue.

### 💪 Strength
- Quickly increases flow volume.

### 🧱 Weakness
- Per-iteration cost is higher than BFS.

---

## 🔍 4. Capacity Scaling

### **What it does & how**
- Processes only paths with **residual capacity ≥ Δ**, where Δ starts as a large power of two (e.g., 2ⁿ ≤ max cap), and is halved each round.
- Augments flows only on those "large" paths first, refining later with smaller Δ values.

### **Complexity**
- **O(E² log C)**, where **C** is the largest capacity.

### ✅ Pros
- Efficient use of large-capacity edges early.
- Avoids small, inefficient paths at first.

### ❌ Cons
- More complex implementation.
- Slower when most edges are low capacity.

### 💪 Strength
- Great when capacities vary a lot.

### 🧱 Weakness
- Not ideal for uniformly small capacities.

---

## 🔍 5. Dinic’s Algorithm

### **What it does & how**
- Builds a **level graph** using BFS.
- Uses repeated **DFS** to send **blocking flows** (saturating all shortest paths).
- Repeats until no more augmenting paths exist.

### **Complexity**
- **O(V² × E)** general case.
- **O(E√V)** for unit capacity graphs.

### ✅ Pros
- Very fast in practice.
- Good for dense graphs or networks with small capacity.

### ❌ Cons
- More complex to write.
- May be overkill for simple cases.

### 💪 Strength
- Excellent theoretical performance and fast in practice.

### 🧱 Weakness
- Harder to implement, especially blocking flow part.

---





