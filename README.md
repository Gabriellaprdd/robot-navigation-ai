# Robot Pathfinding AI Search Algorithms

Robot Pathfinding AI Search Algorithms is a Python-based AI project that simulates robot navigation through grid-based environments. It implements and compares different search algorithms, including BFS, DFS, GBFS, A*, IDDFS, and Weighted A*, with a visual interface for testing and analysing pathfinding performance.

This project demonstrates core Artificial Intelligence concepts, including graph search, heuristic functions, path reconstruction, state exploration, algorithm comparison, and search optimisation.

## Main Features

- Simulate robot navigation in grid environments
- Load custom map configurations
- Find paths between start and goal positions
- Avoid obstacles and blocked cells
- Visualise explored nodes during searching
- Display the final generated path
- Compare different AI search algorithms
- Support multiple goal locations
- Analyse search efficiency and performance

## Technologies Used

- Python
- Tkinter GUI
- Artificial Intelligence Search Algorithms
- Object-Oriented Programming
- Graph Traversal
- Heuristic Functions
- Priority Queue Implementation
- File Processing

## Search Algorithms Implemented

The project implements several AI search techniques:

## Breadth-First Search (BFS)

BFS explores nodes level by level using a queue structure.

Features:

- Complete search algorithm
- Finds the shortest path in an unweighted grid
- Guarantees optimal solution

---

## Depth-First Search (DFS)

DFS explores one branch deeply before backtracking.

Features:

- Uses stack-based exploration
- Requires less memory compared to BFS
- Useful for comparing uninformed search strategies

---

## Greedy Best-First Search (GBFS)

GBFS uses heuristic information to prioritise nodes that appear closest to the goal.

Uses:

```text
f(n) = h(n)
```

where:

- h(n) = estimated distance to goal

Features:

- Faster exploration
- Goal-directed searching
- Does not always guarantee the shortest path

---

## A* Search Algorithm

A* combines path cost and heuristic estimation to efficiently find optimal paths.

Uses:

```text
f(n) = g(n) + h(n)
```

where:

- g(n) = cost from starting node
- h(n) = estimated distance to goal

Features:

- Optimal pathfinding
- Efficient exploration
- Commonly used in robotics and navigation systems

---

## Iterative Deepening DFS (IDDFS)

IDDFS combines DFS memory efficiency with BFS completeness.

Features:

- Searches using increasing depth limits
- Finds optimal solutions in uniform-cost environments

---

## Weighted A* Search

Weighted A* modifies A* by applying a weight to the heuristic function.

Uses:

```text
f(n) = g(n) + w × h(n)
```

Features:

- Adjustable balance between speed and accuracy
- Allows faster solutions with controlled optimality loss

## Map Representation

Maps are represented using text files containing:

- Grid dimensions
- Robot starting position
- Goal position
- Obstacle locations

The robot navigates through available cells while avoiding blocked positions.

## Algorithm Comparison

| Algorithm | Complete | Optimal | Uses Heuristic |
|---|---|---|---|
| BFS | Yes | Yes | No |
| DFS | No | No | No |
| GBFS | Yes | No | Yes |
| A* | Yes | Yes | Yes |
| IDDFS | Yes | Yes | No |
| Weighted A* | Yes | Depends on weight | Yes |

## Running the Project

## Requirements

To run this project locally:

- Python 3.x
- Tkinter

Recommended:

```text
Python 3.10+
```

## Clone Repository

```bash
git clone https://github.com/Gabriellaprdd/robot-pathfinding-ai.git

cd robot-pathfinding-ai
```

## Run Application

Execute:

```bash
python search.py
```

The GUI application will open and allow users to select maps and run different pathfinding algorithms.

## Testing

The project includes different test maps to evaluate algorithm behaviour.

Tests cover:

- Simple navigation paths
- Obstacle avoidance
- Multiple possible routes
- Unreachable destinations
- Complex environments

Testing focuses on:

- Path correctness
- Algorithm behaviour
- Search efficiency
- Node exploration

## What I Worked On

Through this project, I gained practical experience with:

- Artificial Intelligence search algorithms
- Robot navigation concepts
- Graph traversal techniques
- Heuristic function design
- A* pathfinding implementation
- Weighted search optimisation
- Python object-oriented programming
- GUI development using Tkinter
- Grid environment modelling
- Path reconstruction techniques
- Algorithm performance comparison
- Debugging and testing AI solutions