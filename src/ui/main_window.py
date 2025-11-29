import tkinter as tk
import os

from graph_canvas import GraphCanvas
from controls_panel import ControlsPanel
from models.graph_loader import GraphLoader


class MainWindow:
    """
    Main application window that combines the canvas and control panel.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Social Network Analysis")

        # Graph instance will be loaded from CSV
        self.graph = None

        # Layout: left = canvas, right = controls
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas for drawing the graph
        self.canvas = GraphCanvas(self.left_frame, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Controls panel with buttons
        self.controls = ControlsPanel(
            self.right_frame,
            callbacks={
                "load_sample": self.load_sample_graph,
                "run_bfs": self.run_bfs,
                "run_dfs": self.run_dfs,
                "run_dijkstra": self.run_dijkstra,
                "run_astar": self.run_astar,
                "run_components": self.run_components,
                "run_centrality": self.run_centrality,
                "run_coloring": self.run_coloring,
            }
        )

        self.controls.pack(fill=tk.Y, expand=False)

    def load_sample_graph(self):
        """
        Load the sample_small.csv file from the data folder and draw the graph.
        """

        project_root = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )

        csv_path = os.path.join(project_root, "data", "sample_small.csv")

        print("CSV path:", csv_path)

        self.graph = GraphLoader.load_from_csv(csv_path)
        self.canvas.set_graph(self.graph)
        self.canvas.draw_graph()

    # -------------------------
    # Algorithm Button Handlers
    # -------------------------

    def run_bfs(self):
        from algorithms.bfs import bfs

        if not self.graph:
            print("Load graph first!")
            return

        visited = bfs(self.graph, start_id=1)  # default start node

        print("BFS order:", visited)

        # Clear and redraw graph
        self.canvas.draw_graph()

        # Highlight BFS order
        self.canvas.highlight_nodes(visited, color="yellow")


    def run_dfs(self):
        from algorithms.dfs import dfs

        if not self.graph:
            print("Load graph first!")
            return

        visited = dfs(self.graph, start_id=1)  # default start node
        print("DFS order:", visited)

        # Redraw the base graph
        self.canvas.draw_graph()

        # Highlight DFS result
        self.canvas.highlight_nodes(visited, color="orange")


    def run_dijkstra(self):
        from algorithms.dijkstra import dijkstra, reconstruct_path

        if not self.graph:
            print("Load graph first!")
            return

        start = 1
        goal = 10

        distances, previous = dijkstra(self.graph, start)
        path = reconstruct_path(previous, start, goal)

        print("Shortest path:", path)

        # Show the shortest path visually
        self.canvas.highlight_path(path, node_color="lightgreen", edge_color="blue")


    def run_astar(self):
        from algorithms.astar import astar

        if not self.graph:
            print("Load graph first!")
            return

        start = 1
        goal = 10

        distances, previous, path = astar(self.graph, start, goal)

        print("A* shortest path:", path)

        # Highlight the result
        self.canvas.highlight_path(path, node_color="lightgreen", edge_color="purple")


    def run_components(self):
        from algorithms.connected_components import connected_components

        if not self.graph:
            print("Load graph first!")
            return

        comps = connected_components(self.graph)
        print("Components:", comps)

        self.canvas.highlight_components(comps)

    def run_centrality(self):
        from algorithms.degree_centrality import degree_centrality

        if not self.graph:
            print("Load graph first!")
            return

        results = degree_centrality(self.graph, top_n=5)
        print("Top central nodes:", results)

        # Show results visually
        nodes_to_highlight = [nid for nid, deg in results]
        self.canvas.highlight_nodes(nodes_to_highlight, color="orange")

        # Show as popup table
        self.show_table_popup("Top 5 Degree Centrality", results)


    def run_coloring(self):
        from algorithms.welsh_powell import welsh_powell

        if not self.graph:
            print("Load graph first!")
            return

        coloring = welsh_powell(self.graph)
        print("Coloring:", coloring)

        self.canvas.highlight_coloring(coloring)


    def show_table_popup(self, title, data):
        """
        Show results in a popup window as a simple table.
        data: list of tuples (node_id, value)
        """
        popup = tk.Toplevel(self.root)
        popup.title(title)

        for i, (nid, val) in enumerate(data):
            tk.Label(popup, text=f"Node {nid}", font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5)
            tk.Label(popup, text=str(val), font=("Arial", 12)).grid(row=i, column=1, padx=10, pady=5)

