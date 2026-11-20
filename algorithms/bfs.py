from collections import deque
from node import Node, DIRECTIONS, is_valid

# Breadth-First Search (BFS) algorithm for grid-based navigation
def bfs(n, m, start, goals, walls):
    # Initialize the frontier as a queue (FIFO) with the starting node
    frontier = deque([Node(*start)])
    frontier_set = {start}  # Set for quick membership check of frontier positions
    expanded = set()        # Set to track explored positions
    nodes_expanded = 0      # Counter for number of nodes expanded

    # Main BFS loop
    while frontier:
        current = frontier.popleft()            # Remove node from the front of the queue
        current_pos = (current.x, current.y)
        frontier_set.discard(current_pos)       # Remove position from the frontier set

        if current_pos in expanded:
            continue  # Skip if already expanded

        expanded.add(current_pos)
        nodes_expanded += 1

        # Check if goal reached
        if current_pos in goals:
            return current, nodes_expanded, frontier_set, expanded

        # Explore all valid neighboring positions (up, down, left, right)
        for dx, dy, action in DIRECTIONS:
            nx, ny = current.x + dx, current.y + dy
            next_pos = (nx, ny)

            # Check if neighbor is valid and hasn't been explored or added to the frontier yet
            if (
                is_valid(nx, ny, n, m, walls)
                and next_pos not in expanded
                and next_pos not in frontier_set
            ):
                # Add valid neighbor to the end of the queue
                frontier.append(Node(nx, ny, current, action))
                frontier_set.add(next_pos)

    # No solution found
    return None, nodes_expanded, frontier_set, expanded
