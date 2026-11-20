import heapq
from node import Node, DIRECTIONS, is_valid

# Heuristic function: Manhattan distance to the nearest goal
def heuristic_manhattan(x, y, goals):
    return min(abs(x - gx) + abs(y - gy) for gx, gy in goals)

# Greedy Best-First Search (GBFS) algorithm
def gbfs(n, m, start, goals, walls):
    # Initialize priority queue (min-heap) for the frontier, ordered by heuristic value
    frontier = []
    start_node = Node(*start, heuristic=heuristic_manhattan(*start, goals))
    heapq.heappush(frontier, start_node) # https://docs.python.org/3/library/heapq.html (reference)
    
    frontier_set = {start}  # Set for quick membership checks
    expanded = set()        # Track already-explored positions
    nodes_expanded = 0      # Count of nodes expanded for stats

    # Main GBFS loop
    while frontier:
        current = heapq.heappop(frontier)       # Always pick the node with the lowest heuristic
        current_pos = (current.x, current.y)
        frontier_set.discard(current_pos)       # Remove from the frontier set

        if current_pos in expanded:
            continue  # Skip if already explored

        expanded.add(current_pos)
        nodes_expanded += 1

        # Check if we've reached a goal
        if current_pos in goals:
            return current, nodes_expanded, frontier_set, expanded

        # Explore neighbors (up, down, left, right)
        for dx, dy, action in DIRECTIONS:
            nx, ny = current.x + dx, current.y + dy
            next_pos = (nx, ny)

            # Only add valid and unexplored neighbors
            if is_valid(nx, ny, n, m, walls) and next_pos not in expanded and next_pos not in frontier_set:
                h = heuristic_manhattan(nx, ny, goals)
                # In GBFS, the path cost is ignored (set to 0); only heuristic matters
                heapq.heappush(frontier, Node(nx, ny, current, action, 0, h))
                frontier_set.add(next_pos)

    # No solution found
    return None, nodes_expanded, frontier_set, expanded
