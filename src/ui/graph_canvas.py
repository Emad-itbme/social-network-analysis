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
        self.component_colors = [
         "lightgreen", "lightblue", "lightpink", "khaki",
         "plum", "lightsalmon", "wheat", "lightgray"
        ]
        self.color_palette = [
            "lightgreen", "lightblue", "lightpink", "khaki",
            "plum", "lightsalmon", "wheat", "lightgray",
            "lightcoral", "lightsteelblue", "aquamarine"
        ]
        self.bind("<Button-1>", self.on_click)
        self.click_callback = None




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

    def highlight_nodes(self, nodes, color="yellow"):
        """
        Highlights a list of nodes with a given color.
        """
        if not self.node_positions:
            return
        
        r = self.node_radius

        for node_id in nodes:
            if node_id in self.node_positions:
                x, y = self.node_positions[node_id]

                # Draw a highlight circle behind the node
                self.create_oval(
                    x - r - 6, y - r - 6,
                    x + r + 6, y + r + 6,
                    fill=color, outline=""
                )

        # Redraw nodes on top
        for node_id, (x, y) in self.node_positions.items():
            self.create_oval(
                x - r, y - r, x + r, y + r,
                fill="lightblue", outline="black"
            )
            self.create_text(x, y, text=str(node_id))

    def highlight_path(self, path, node_color="lightgreen", edge_color="blue"):
        
        """
        Highlights a specific path (list of node IDs).
        Colors nodes and edges along the path.
        """

        if not path or len(path) < 2:
            return

        # Redraw graph first
        self.draw_graph()

        r = self.node_radius

        # Highlight nodes on the path
        for node_id in path:
            if node_id in self.node_positions:
                x, y = self.node_positions[node_id]
                self.create_oval(
                    x - r - 6, y - r - 6,
                    x + r + 6, y + r + 6,
                    fill=node_color, outline=""
                )

        # Highlight edges on the path
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]

            if u in self.node_positions and v in self.node_positions:
                x1, y1 = self.node_positions[u]
                x2, y2 = self.node_positions[v]

                # Draw highlighted edge on top
                self.create_line(
                    x1, y1, x2, y2,
                    fill=edge_color,
                    width=3
                )

        # Redraw nodes text on top
        for node_id, (x, y) in self.node_positions.items():
            self.create_oval(
                x - r, y - r, x + r, y + r,
                fill="lightblue", outline="black"
            )
            self.create_text(x, y, text=str(node_id))

    def highlight_coloring(self, coloring):
        """
        Apply graph coloring (node_id -> color_index) to the canvas.
        """
        self.draw_graph()

        r = self.node_radius

        for node_id, color_idx in coloring.items():
            if node_id in self.node_positions:
                color = self.color_palette[color_idx % len(self.color_palette)]
                x, y = self.node_positions[node_id]

                self.create_oval(
                    x - r - 6, y - r - 6,
                    x + r + 6, y + r + 6,
                    fill=color, outline=""
                )

        # Redraw nodes on top
        for node_id, (x, y) in self.node_positions.items():
            self.create_oval(
                x - r, y - r, x + r, y + r,
                fill="lightblue", outline="black"
            )
            self.create_text(x, y, text=str(node_id))

    def highlight_components(self, components):
        """
        Color each connected component with a different color.
        components: list of lists (each component is a list of node IDs)
        """
        self.draw_graph()

        r = self.node_radius

        for index, comp in enumerate(components):
            color = self.component_colors[index % len(self.component_colors)]

            for node_id in comp:
                if node_id in self.node_positions:
                    x, y = self.node_positions[node_id]
                    self.create_oval(
                        x - r - 6, y - r - 6,
                        x + r + 6, y + r + 6,
                        fill=color, outline=""
                    )

        # Redraw nodes on top
        for node_id, (x, y) in self.node_positions.items():
            self.create_oval(
                x - r, y - r, x + r, y + r,
                fill="lightblue", outline="black"
            )
            self.create_text(x, y, text=str(node_id))
    def on_click(self, event):
        """Detect which node was clicked."""
        x, y = event.x, event.y

        for node_id, (nx, ny) in self.node_positions.items():
            r = self.node_radius
            if (x - nx) ** 2 + (y - ny) ** 2 <= r ** 2:
                if self.click_callback:
                    self.click_callback(node_id)
                break
    def set_click_callback(self, callback):
        self.click_callback = callback
