import tkinter as tk
from tkinter import filedialog, messagebox
import os
import time

# Import search algorithms (assumed to be implemented separately)
from algorithms import bfs, dfs, gbfs, astar, iddfs, wastar
from node import Node, DIRECTIONS, is_valid

# Function to safely parse the text file describing the grid, start, goals, and walls
def parse_input_file(filepath):
    try:
        with open(filepath, 'r') as file:
            # Read and clean lines, ignoring empty lines
            lines = [line.strip() for line in file if line.strip()]
        # Extract grid size, start position, goals, and walls
        n, m = map(int, lines[0].split('x'))
        start = tuple(map(int, lines[1].split(',')))
        goals = [tuple(map(int, goal.split(','))) for goal in lines[2].split(';')]
        walls = {tuple(map(int, line.split(','))) for line in lines[3:]}
        return n, m, start, goals, walls
    except Exception as e:
        raise ValueError(f"Invalid file format: {e}")

# Custom Canvas widget for visualizing the grid and search process
class GridVisualizer(tk.Canvas):
    def __init__(self, master, n, m, start, goals, walls):
        super().__init__(master, width=40*n, height=40*m, bg="white")
        self.pack()
        self.n, self.m = n, m
        self.start, self.goals, self.walls = start, set(goals), walls
        self.rects = {}  # Dictionary to keep track of cell rectangles
        self.draw_static_grid()

    # Draw the initial grid: start, goals, walls, and labels
    def draw_static_grid(self):
        for y in range(self.m):
            for x in range(self.n):
                pos = (x, y)
                color = "white"
                if pos in self.walls:
                    color = "#bbbbbb"  # Wall
                elif pos == self.start:
                    color = "#ff746c"  # Start
                elif pos in self.goals:
                    color = "#80ef80"  # Goal
                # Draw cell rectangle
                self.rects[pos] = self.create_rectangle(
                    x*40, y*40, (x+1)*40, (y+1)*40,
                    fill=color, outline="#e11b95"
                )
                # Draw cell coordinates for clarity
                self.create_text(
                    x*40 + 20, y*40 + 10,
                    text=f"{x},{y}",
                    font=("Times New Roman", 8, "bold italic")
                )

    # Reset grid colors (useful before starting a new search)
    def reset_grid(self):
        for y in range(self.m):
            for x in range(self.n):
                pos = (x, y)
                color = "white"
                if pos in self.walls:
                    color = "#bbbbbb"
                elif pos == self.start:
                    color = "#ff746c"
                elif pos in self.goals:
                    color = "#80ef80"
                self.itemconfig(self.rects[pos], fill=color)

    # Animate search progress: expanded nodes (yellow) and frontier (orange)
    def animate_search_progress(self, expanded_set, frontier_set, callback=None):
        expanded = sorted(expanded_set, key=lambda p: (p[1], p[0]))
        frontier = sorted(p for p in frontier_set if p not in expanded_set)

        def animate_nodes(nodes, color, index=0, delay=60, next_step=None):
            if index < len(nodes):
                pos = nodes[index]
                if pos != self.start and pos not in self.goals:
                    self.itemconfig(self.rects[pos], fill=color)
                self.after(delay, lambda: animate_nodes(nodes, color, index+1, delay, next_step))
            elif next_step:
                self.after(300, next_step)  # Small pause before next step

        # Animate expanded nodes, then frontier, then trigger callback (like drawing the path)
        animate_nodes(expanded, "#fdfd96", delay=60,
                      next_step=lambda: animate_nodes(frontier, "#ffd6a5", delay=50, next_step=callback))

    # Draw the final solution path in blue
    def draw_path(self, path, animate=True):
        def animate_path(index=0):
            if index < len(path):
                pos = path[index]
                if pos != self.start and pos not in self.goals:
                    self.itemconfig(self.rects[pos], fill="#abcbff")
                self.after(100, lambda: animate_path(index + 1))
        if animate:
            animate_path()
        else:
            for pos in path:
                if pos != self.start and pos not in self.goals:
                    self.itemconfig(self.rects[pos], fill="#abcbff")

# The main application class that ties everything together
class SearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Navigation Search")

        # Available search methods mapped to their functions
        self.methods = {
            "BFS": bfs.bfs,
            "DFS": dfs.dfs,
            "GBFS": gbfs.gbfs,
            "AS": astar.astar,
            "IDDFS": iddfs.iddfs,
            "WAS": wastar.wastar
        }

        self.filepath = None
        self.grid = None
        self.n = self.m = 0
        self.start = ()
        self.goals = []
        self.walls = set()

        self.build_interface()

    # Set up the GUI layout
    def build_interface(self):
        # File selection button
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)
        tk.Button(top_frame, text="Select Text File",
                  command=self.load_file, font=("Times New Roman", 10),
                  bg="#f3c3ff", fg="#9428af", padx=10).pack()

        # Label for status messages (search results, errors, etc.)
        self.msg_label = tk.Label(self.root, text="", fg="#e11b95",
                                  font=("Times New Roman", 10), wraplength=500, justify="left")
        self.msg_label.pack(pady=10)

        # Placeholder for the grid
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack()

        # Legend showing the meaning of colors
        legend_frame = tk.Frame(self.root)
        legend_frame.pack(pady=(10, 5))
        legend_items = [
            ("#ff746c", "Start"), ("#80ef80", "Goal"),
            ("#bbbbbb", "Wall"), ("#fdfd96", "Expanded"),
            ("#ffd6a5", "Frontier"), ("#abcbff", "Path")
        ]
        for color, label in legend_items:
            item_frame = tk.Frame(legend_frame)
            item_frame.pack(side="left", padx=8)
            canvas = tk.Canvas(item_frame, width=20, height=20)
            canvas.create_rectangle(0, 0, 20, 20, fill=color, outline="black")
            canvas.pack(side="left")
            tk.Label(item_frame, text=label, font=("Times New Roman", 10)).pack(side="left", padx=4)

        # Buttons to run different search algorithms
        algo_frame = tk.Frame(self.root)
        algo_frame.pack(pady=10)
        for method in self.methods:
            tk.Button(algo_frame, text=method, command=lambda m=method: self.run_search(m),
                      width=8, bg="#ffb4e2", font=("Times New Roman", 10), fg="#e11b95").pack(side="left", padx=5)

    # Load grid data from a file
    def load_file(self):
        self.filepath = filedialog.askopenfilename(
            title="Select Text File", filetypes=[("Text files", "*.txt")]
        )
        if not self.filepath:
            return
        try:
            self.n, self.m, self.start, self.goals, self.walls = parse_input_file(self.filepath)
            if self.grid:
                self.grid.destroy()  # Clear previous grid if any
            self.grid = GridVisualizer(self.canvas_frame, self.n, self.m, self.start, self.goals, self.walls)
            self.msg_label.config(text="Please select an algorithm to begin.")
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to load file: {e}")

    # Run the selected search algorithm
    def run_search(self, method):
        if not self.filepath:
            messagebox.showwarning("No File", "Please load a text file first.")
            return

        self.grid.reset_grid()
        search_fn = self.methods[method]
        self.start_time = time.time()
        result = search_fn(self.n, self.m, self.start, self.goals, self.walls)

        if result is None or len(result) < 4:
            self.msg_label.config(text=f"{method} failed or returned invalid output.")
            return

        goal_node, nodes_expanded, frontier_set, expanded_set = result

        # Display final results after search completes
        def show_results():
            elapsed_time = time.time() - self.start_time
            if goal_node:
                path = []
                node = goal_node
                while node:
                    path.append((node.x, node.y))
                    node = node.parent
                path.reverse()
                self.grid.draw_path(path)

                # Get human-readable directions
                directions = []
                for (x1, y1), (x2, y2) in zip(path, path[1:]):
                    if x2 == x1 + 1: directions.append("right")
                    elif x2 == x1 - 1: directions.append("left")
                    elif y2 == y1 + 1: directions.append("down")
                    elif y2 == y1 - 1: directions.append("up")

                self.msg_label.config(
                    text=f"{os.path.basename(self.filepath)} {method}\n"
                         f"Start at {self.start}\n"
                         f"Goal at ({goal_node.x},{goal_node.y})\n"
                         f"{nodes_expanded} nodes expanded\n"
                         f"{'; '.join(directions)}\n"
                         f"Time taken: {elapsed_time:.4f} seconds"
                )
            else:
                self.msg_label.config(
                    text=f"{os.path.basename(self.filepath)} {method}\n"
                         f"Start at {self.start}\n"
                         f"No solution found.\n"
                         f"{nodes_expanded} nodes expanded\n"
                         f"Time taken: {elapsed_time:.4f} seconds"
                )

        # Animate the search progress and then show the results
        self.grid.animate_search_progress(expanded_set, frontier_set, callback=show_results)

# Start the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()
