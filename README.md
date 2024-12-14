
# AI Maze Solver and Generator

This project implements a graphical tool for generating and solving mazes using three fundamental search algorithms: **A\*** (A-Star Search), **Uniform Cost Search (UCS)**, and **Best-First Search (BFS)**. It provides a user-friendly graphical user interface (GUI) for generating, customizing, and solving mazes.

---

## Features

### Maze Generation
- Generate **random mazes** with walls and weighted paths.
- **Manually customize** mazes by adding walls, start points, and up to two goal points directly through the GUI.

### Maze Solving Algorithms
- **A\*** Search: Uses a combination of path cost and heuristic for optimal pathfinding.
- **Uniform Cost Search (UCS)**: Finds the least-cost path using only path cost.
- **Best-First Search (BFS)**: Prioritizes nodes with the lowest heuristic value.
- Selection between **Manhattan distance** and **Euclidean distance** as the heuristic.

### Visualization
- Display the **maze grid** with visual feedback for walls which is represented as "-1" in the code, start points, goals, and solution paths.
- Show the **number of steps** in the solution and the **number of nodes tested**.

---

## Installation

### Prerequisites
- Python 3.7 or higher
- Required libraries: `tkinter`, `math`, `heapq`

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/mkittani/AI-Maze-Solver-and-Generator.git

2. Install libraries (if needed):
   ```bash
   pip install tk
3. Run the program:
   ```bash
   python main.py

