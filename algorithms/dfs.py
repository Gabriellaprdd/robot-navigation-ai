from node import Node, DIRECTIONS, is_valid

# Depth-First Search (DFS) algorithm for grid navigation
def dfs(n, m, start, goals, walls):
    # Use a stack (LIFO) for the frontier; start with the starting node
    frontier = [Node(*start)]
    frontier_set = {start}  # Track positions in the frontier for quick checks
    expanded = set()        # Track positions we've already explored
    nodes_expanded = 0      # Count of nodes expanded for stats/visualization

    # Main DFS loop
    while frontier:
        current = frontier.pop()                # Pop from end of list (LIFO for DFS)
        current_pos = (current.x, current.y)
        frontier_set.discard(current_pos)       # Remove position from the frontier set

        if current_pos in expanded:
            continue  # Skip if already explored

        expanded.add(current_pos)
        nodes_expanded += 1

        # Check if we've reached any goal
        if current_pos in goals:
            return current, nodes_expanded, frontier_set, expanded

        # Add neighbors in reversed order for consistent traversal order
        for dx, dy, action in reversed(DIRECTIONS):
            nx, ny = current.x + dx, current.y + dy
            next_pos = (nx, ny)

            # Only add valid, unexplored neighbors to the frontier
            if (
                is_valid(nx, ny, n, m, walls) 
                and next_pos not in expanded 
                and next_pos not in frontier_set
            ):
                frontier.append(Node(nx, ny, current, action))
                frontier_set.add(next_pos)

    # No solution found
    return None, nodes_expanded, frontier_set, expanded
