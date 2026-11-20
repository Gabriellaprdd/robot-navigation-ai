from node import Node, DIRECTIONS, is_valid

# Recursive Depth-Limited Search (DLS) function
def dls(n, m, node, goals, walls, limit, expanded_set, frontier_set):
    pos = (node.x, node.y)
    expanded_set.add(pos)      # Mark current node as expanded
    frontier_set.discard(pos)  # Remove from frontier since it's being expanded

    # If we reach a goal, return the node (path found)
    if pos in goals:
        return node

    # If we reach the depth limit, stop exploring further
    if limit <= 0:
        return None

    # Explore neighboring cells (up, down, left, right)
    for dx, dy, action in DIRECTIONS:
        nx, ny = node.x + dx, node.y + dy
        next_pos = (nx, ny)

        # Only explore valid and unexplored neighbors
        if is_valid(nx, ny, n, m, walls) and next_pos not in expanded_set:
            frontier_set.add(next_pos)
            child = Node(nx, ny, node, action)  # Create a new node for the neighbor
            found = dls(n, m, child, goals, walls, limit - 1, expanded_set, frontier_set)
            if found:
                return found  # If a solution is found in recursion, return it

    # No solution found at this depth
    return None

# Iterative Deepening DFS (IDDFS) driver function
def iddfs(n, m, start, goals, walls):
    depth = 0  # Start with depth 0 and incrementally deepen
    total_expanded = set()  # Track all nodes expanded across iterations
    total_frontier = set()  # Track the last frontier set for visualization

    # Keep deepening the search until we reach the theoretical max depth (grid size)
    while depth <= n * m:
        expanded_set = set()     # Nodes expanded at this depth
        frontier_set = {start}   # Start position is initially in the frontier

        result = dls(n, m, Node(*start), goals, walls, depth, expanded_set, frontier_set)
        total_expanded.update(expanded_set)  # Collect all expanded nodes
        total_frontier = frontier_set        # Update frontier for visualization

        if result:
            return result, len(total_expanded), total_frontier, total_expanded

        depth += 1  # Increase depth limit and try again

    # No solution found after full search
    return None, len(total_expanded), total_frontier, total_expanded
