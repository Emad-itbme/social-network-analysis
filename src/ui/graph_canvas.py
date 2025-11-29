import tkinter as tk
import math


class GraphCanvas(tk.Canvas):
    """
    Canvas widget responsible for drawing the graph (nodes + edges).
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.graph = None
        self.node_positions = {}  # node_id -> (x, y)
        self.node_radius = 20

    def set_graph(self, graph):
        """Attach a Graph instance to this canvas."""
        self.graph = graph

    def draw_graph(self):
        """Clear the canvas and draw the current graph."""
        self.delete("all")
        self.node_positions.clear()

        if self.graph is None or not self.graph.nodes:
            return

        # Determine canvas size
        try:
            width = self.winfo_width()
            height = self.winfo_height()
            if width <= 1 or height <= 1:
                # Fallback to configured size if widget not yet fully rendered
                width = int(self["width"])
                height = int(self["height"])
        except Exception:
            width = 800
            height = 600

        center_x = width // 2
        center_y = height // 2
        radius = min(width, height) // 2 - 60

        node_ids = sorted(self.graph.nodes.keys())
        n = len(node_ids)

        # Compute positions on a circle
        for index, node_id in enumerate(node_ids):
            angle = 2 * math.pi * index / n
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.node_positions[node_id] = (x, y)

        # Draw edges first
        for edge in self.graph.get_edges():
            u = edge.u
            v = edge.v
            if u in self.node_positions and v in self.node_positions:
                x1, y1 = self.node_positions[u]
                x2, y2 = self.node_positions[v]
                self.create_line(x1, y1, x2, y2, fill="gray")

        # Draw nodes on top
        r = self.node_radius
        for node_id, (x, y) in self.node_positions.items():
            self.create_oval(x - r, y - r, x + r, y + r,
                             fill="lightblue", outline="black")
            self.create_text(x, y, text=str(node_id))
