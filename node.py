# Directions for grid movement: (dx, dy, action_name)
# Right (+1, 0), Down (0, +1), Left (-1, 0), Up (0, -1)
DIRECTIONS = [
    (1, 0, 'right'),
    (0, 1, 'down'),
    (-1, 0, 'left'),
    (0, -1, 'up')
]

# Checks if a grid position is valid (inside grid bounds and not a wall)
def is_valid(x, y, n, m, walls):
    return 0 <= x < n and 0 <= y < m and (x, y) not in walls

# Node class for search algorithms (e.g., A*, BFS, DFS)
class Node:
    def __init__(self, x, y, parent=None, action=None, cost=0, heuristic=0):
        self.x = x                  # x-coordinate in grid
        self.y = y                  # y-coordinate in grid
        self.parent = parent        # Reference to parent Node (for path reconstruction)
        self.action = action        # Action taken to reach this node ('right', 'down', etc.)
        self.cost = cost            # Path cost (g-value)
        self.heuristic = heuristic  # Heuristic value (h-value)

    # Comparison method for priority queues (e.g., heapq)
    # Nodes are ordered by f = g + h
    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    # Reconstruct the path from start to current node by backtracking parents
    def path(self):
        node, p = self, []
        while node.parent:
            p.append(node.action)
            node = node.parent
        return p[::-1]  # Reverse the action list to get correct order (start to goal)
