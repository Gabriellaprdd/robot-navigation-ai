import heapq
from itertools import count
from node import Node, DIRECTIONS, is_valid

# Heuristic function: Manhattan distance to the closest goal
def heuristic_manhattan(x, y, goals):
    return min(abs(x - gx) + abs(y - gy) for gx, gy in goals)

# A* search algorithm
def astar(n, m, start, goals, walls):
    # Priority queue (min-heap) for frontier nodes: (f_score, unique_id, node)
    frontier = []
    counter = count()  # Tie-breaker for heap (ensures unique order)
    start_h = heuristic_manhattan(*start, goals)  # Heuristic for start position
    start_node = Node(*start, cost=0, heuristic=start_h)
    heapq.heappush(frontier, (start_node.cost + start_h, next(counter), start_node))

    # Tracks the lowest cost to reach each position
    cost_so_far = {start: 0}

    # Expanded and frontier node tracking for visualization and analysis
    expanded = set()  # Explored nodes
    frontier_set = {start}  # Current frontier nodes
    nodes_expanded = 0  # Counter for expanded nodes

    # Main A* search loop
    while frontier:
        _, _, current = heapq.heappop(frontier)
        current_pos = (current.x, current.y)
        frontier_set.discard(current_pos)  # Remove from frontier

        # Skip if already expanded
        if current_pos in expanded:
            continue

        expanded.add(current_pos)
        nodes_expanded += 1

        # Goal check
        if current_pos in goals:
            return current, nodes_expanded, frontier_set, expanded

        # Explore neighbors (up, down, left, right)
        for dx, dy, action in DIRECTIONS:
            nx, ny = current.x + dx, current.y + dy
            next_pos = (nx, ny)

            if not is_valid(nx, ny, n, m, walls):
                continue  # Skip invalid moves (out of bounds or into wall)

            new_cost = current.cost + 1  # Uniform cost for each step

            # If this path is better (lower cost), update and add to frontier
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                h = heuristic_manhattan(nx, ny, goals)  # Heuristic estimate
                next_node = Node(nx, ny, current, action, new_cost, h)
                heapq.heappush(frontier, (new_cost + h, next(counter), next_node))
                frontier_set.add(next_pos)

    # No solution found
    return None, nodes_expanded, frontier_set, expanded
