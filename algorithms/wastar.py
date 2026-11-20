import heapq
from node import Node, DIRECTIONS, is_valid

# Manhattan distance heuristic for grid-based problems
def heuristic_manhattan(x, y, goals):
    return min(abs(x - gx) + abs(y - gy) for gx, gy in goals)

# Weighted A* Search (WA*) algorithm
def wastar(n, m, start, goals, walls, w=1.5):
    frontier = []  # Priority queue for nodes to explore (min-heap)
    
    # Compute weighted heuristic for the start node
    start_h = w * heuristic_manhattan(*start, goals)
    start_node = Node(*start, cost=0, heuristic=start_h)
    
    # Add start node to the frontier with priority = f = g + h
    heapq.heappush(frontier, (start_node.cost + start_h, start_node)) # https://docs.python.org/3/library/heapq.html (reference)
    
    # Sets and dictionaries for bookkeeping
    frontier_set = {start}       # Tracks nodes currently in the frontier
    cost_so_far = {start: 0}     # g-values (actual cost from start)
    expanded = set()             # Expanded nodes
    nodes_expanded = 0           # Counter for number of expanded nodes

    while frontier:
        _, current = heapq.heappop(frontier)
        current_pos = (current.x, current.y)
        frontier_set.discard(current_pos)  # Remove from frontier as we're expanding it

        # Skip if already expanded (avoid duplicates)
        if current_pos in expanded:
            continue

        expanded.add(current_pos)
        nodes_expanded += 1

        # Check for goal
        if current_pos in goals:
            return current, nodes_expanded, frontier_set, expanded

        # Explore neighboring cells (up, down, left, right)
        for dx, dy, action in DIRECTIONS:
            nx, ny = current.x + dx, current.y + dy
            next_pos = (nx, ny)

            if not is_valid(nx, ny, n, m, walls):
                continue

            new_cost = current.cost + 1  # Uniform step cost of 1 per move
            # Update if we find a better path (lower g-cost)
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                h = w * heuristic_manhattan(nx, ny, goals)  # Apply weight to heuristic
                next_node = Node(nx, ny, current, action, new_cost, h)
                heapq.heappush(frontier, (new_cost + h, next_node))
                frontier_set.add(next_pos)

    # If no solution found, return None and stats
    return None, nodes_expanded, frontier_set, expanded
