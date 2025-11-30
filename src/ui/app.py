import os
import sys
import math
import tkinter as tk
import customtkinter as ctk

# -------------------------------------------------
# Make src package visible (models, algorithms ...)
# -------------------------------------------------
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from models.graph import Graph
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dijkstra import dijkstra, reconstruct_path
from algorithms.astar import astar
from algorithms.connected_components import connected_components
from algorithms.degree_centrality import degree_centrality
from algorithms.welsh_powell import welsh_powell


class SocialNetworkUI:
    def __init__(self, root: ctk.CTk):
        self.root = root

        # ----- core graph -----
        self.graph = Graph()
        self.node_radius = 22
        self.node_positions: dict[int, tuple[float, float]] = {}
        self.node_items: dict[int, tuple[int, int]] = {}  # node_id -> (circle_id, text_id)
        self.edge_items: dict[frozenset, int] = {}        # {u,v} -> line_id
        self.next_node_id = 1
        self.selected_node: int | None = None  # for edge creation

        # ----- main layout -----
        self.root.title("Social Network Analysis - Modern UI")
        self.root.geometry("1400x800")

        self.main_frame = ctk.CTkFrame(root, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        # Left: canvas container
        self.canvas_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.canvas_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg="#15161E",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Right: sidebar
        self.sidebar = ctk.CTkFrame(self.main_frame, corner_radius=10, width=260)
        self.sidebar.pack(side="right", fill="y", padx=10, pady=10)

        self.build_sidebar()

        # Status bar
        self.status_label = ctk.CTkLabel(
            root,
            text="Click on canvas to add a person.",
            anchor="w"
        )
        self.status_label.pack(fill="x", padx=10, pady=(0, 8))

        # Bind canvas click
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    # ------------------------------------------------------------------
    # UI BUILD
    # ------------------------------------------------------------------
    def build_sidebar(self):
        title = ctk.CTkLabel(
            self.sidebar,
            text="Algorithms",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(10, 5))

        self.start_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Start node id (default 1)")
        self.start_entry.pack(pady=(0, 10), padx=10, fill="x")

        btn_cfg = {"height": 32, "corner_radius": 6}

        ctk.CTkButton(self.sidebar, text="BFS",
                      command=self.run_bfs, **btn_cfg).pack(pady=4, padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="DFS",
                      command=self.run_dfs, **btn_cfg).pack(pady=4, padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Dijkstra",
                      command=self.run_dijkstra, **btn_cfg).pack(pady=4, padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="A* ",
                      command=self.run_astar, **btn_cfg).pack(pady=4, padx=10, fill="x")

        ctk.CTkButton(self.sidebar, text="Components",
                      command=self.run_components, **btn_cfg).pack(pady=(12, 4), padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Centrality",
                      command=self.run_centrality, **btn_cfg).pack(pady=4, padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Graph Coloring",
                      command=self.run_coloring, **btn_cfg).pack(pady=4, padx=10, fill="x")

        ctk.CTkLabel(self.sidebar, text=" ", height=10).pack()  # spacer

        ctk.CTkButton(self.sidebar, text="Load sample CSV",
                      command=self.load_sample_graph, **btn_cfg).pack(pady=4, padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Clear graph",
                      fg_color="#a83232",
                      hover_color="#7a2020",
                      command=self.clear_graph, **btn_cfg).pack(pady=(8, 4), padx=10, fill="x")

    # ------------------------------------------------------------------
    # Canvas interactions
    # ------------------------------------------------------------------
    def on_canvas_click(self, event):
        x, y = event.x, event.y
        clicked_id = self.get_node_at(x, y)

        # If click on empty space → create person popup
        if clicked_id is None:
            self.open_node_popup(x, y)
            return

        # If click on node: either start or end of edge
        if self.selected_node is None:
            self.selected_node = clicked_id
            self.highlight_node_border(clicked_id, outline="#ffcc00", width=3)
            self.status_label.configure(text=f"Selected node {clicked_id}. Click another node to connect.")
        else:
            if clicked_id != self.selected_node:
                self.create_edge(self.selected_node, clicked_id)
                self.status_label.configure(
                    text=f"Edge created between {self.selected_node} and {clicked_id}."
                )
            # reset selection
            self.highlight_node_border(self.selected_node, outline="#ffffff", width=1)
            self.selected_node = None

    def get_node_at(self, x, y):
        for nid, (circle, _) in self.node_items.items():
            cx, cy = self.node_positions[nid]
            if (x - cx) ** 2 + (y - cy) ** 2 <= self.node_radius ** 2:
                return nid
        return None

    # ------------------------------------------------------------------
    # Node creation popup
    # ------------------------------------------------------------------
    def open_node_popup(self, x, y):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Add Person")
        popup.geometry("300x260")
        popup.grab_set()  # modal

        ctk.CTkLabel(popup, text="Create new person", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        name_entry = ctk.CTkEntry(popup, placeholder_text="Name (optional)")
        name_entry.pack(pady=4, padx=20, fill="x")

        act_entry = ctk.CTkEntry(popup, placeholder_text="Activity (0-1)")
        act_entry.pack(pady=4, padx=20, fill="x")

        inter_entry = ctk.CTkEntry(popup, placeholder_text="Interaction (e.g. 10)")
        inter_entry.pack(pady=4, padx=20, fill="x")

        conn_entry = ctk.CTkEntry(popup, placeholder_text="Connection count")
        conn_entry.pack(pady=4, padx=20, fill="x")

        error_label = ctk.CTkLabel(popup, text="", text_color="red")
        error_label.pack(pady=2)

        def on_confirm():
            try:
                name = name_entry.get().strip() or f"User {self.next_node_id}"
                activity = float(act_entry.get() or 0.5)
                interaction = float(inter_entry.get() or 0.0)
                conn_count = float(conn_entry.get() or 0.0)
            except ValueError:
                error_label.configure(text="Please enter numeric values for activity/interaction/connections.")
                return

            popup.destroy()
            self.create_node(x, y, name, activity, interaction, conn_count)

        btn_frame = ctk.CTkFrame(popup)
        btn_frame.pack(pady=10, fill="x")

        ctk.CTkButton(btn_frame, text="Cancel", command=popup.destroy).pack(side="left", padx=10, expand=True)
        ctk.CTkButton(btn_frame, text="Create", command=on_confirm).pack(side="right", padx=10, expand=True)

    def create_node(self, x, y, name, activity, interaction, connection_count):
        nid = self.next_node_id
        self.next_node_id += 1

        # Update backend Graph (social network node)
        self.graph.add_node(
            nid,
            name=name,
            activity=activity,
            interaction=interaction,
            connection_count=connection_count,
        )

        # Draw on canvas
        circle = self.canvas.create_oval(
            x - self.node_radius, y - self.node_radius,
            x + self.node_radius, y + self.node_radius,
            fill="#3A5166",
            outline="#ffffff",
            width=1,
        )
        text = self.canvas.create_text(
            x, y, text=str(nid),
            fill="#e5e7eb",
            font=("Segoe UI", 12, "bold")
        )

        self.node_positions[nid] = (x, y)
        self.node_items[nid] = (circle, text)

        self.status_label.configure(text=f"Person {nid} created at ({x}, {y}).")

    def highlight_node_border(self, node_id, outline="#ffffff", width=1):
        circle, _ = self.node_items[node_id]
        self.canvas.itemconfig(circle, outline=outline, width=width)

    def highlight_node_fill(self, node_id, color):
        circle, _ = self.node_items[node_id]
        self.canvas.itemconfig(circle, fill=color)

    def highlight_edge(self, u, v, color, width=3):
        key = frozenset({u, v})
        line_id = self.edge_items.get(key)
        if line_id:
            self.canvas.itemconfig(line_id, fill=color, width=width)

    def create_edge(self, u, v):
        if u == v:
            return

        # Avoid duplicate
        key = frozenset({u, v})
        if key in self.edge_items:
            return

        x1, y1 = self.node_positions[u]
        x2, y2 = self.node_positions[v]
        line_id = self.canvas.create_line(x1, y1, x2, y2, fill="#9CA3AF", width=2)
        self.edge_items[key] = line_id

        # Compute social weight using formula
        n1 = self.graph.nodes[u]
        n2 = self.graph.nodes[v]
        weight = 1.0 / (
            1.0
            + math.sqrt(
                (n1.activity - n2.activity) ** 2
                + (n1.interaction - n2.interaction) ** 2
                + (n1.connection_count - n2.connection_count) ** 2
            )
        )
        self.graph.add_edge(u, v, weight)

    # ------------------------------------------------------------------
    # Graph reset / load
    # ------------------------------------------------------------------
    def clear_graph(self):
        self.canvas.delete("all")
        self.graph = Graph()
        self.node_positions.clear()
        self.node_items.clear()
        self.edge_items.clear()
        self.next_node_id = 1
        self.selected_node = None
        self.status_label.configure(text="Graph cleared. Click on canvas to add persons.")

    def load_sample_graph(self):
        """
        Load your CSV social network and place nodes on a circle.
        """
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(project_root, "data", "sample_small.csv")

        from models.graph_loader import GraphLoader

        self.clear_graph()
        self.graph = GraphLoader.load_from_csv(csv_path)

        # Layout nodes on circle
        width = self.canvas.winfo_width() or 900
        height = self.canvas.winfo_height() or 700
        cx, cy = width // 2, height // 2
        radius = min(width, height) // 2 - 80

        node_ids = sorted(self.graph.nodes.keys())
        n = len(node_ids)

        for i, nid in enumerate(node_ids):
            angle = 2 * math.pi * i / n
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            self.create_node(x, y,
                             self.graph.nodes[nid].name,
                             self.graph.nodes[nid].activity,
                             self.graph.nodes[nid].interaction,
                             self.graph.nodes[nid].connection_count)

        # Draw edges from graph backend
        for edge in self.graph.edges:
            self.create_edge(edge.u, edge.v)

        self.status_label.configure(text="Sample social network loaded from CSV.")

    # ------------------------------------------------------------------
    # Animation helpers
    # ------------------------------------------------------------------
    def reset_visual_style(self):
        # reset nodes
        for nid in self.node_items:
            self.highlight_node_fill(nid, "#3A5166")
            self.highlight_node_border(nid, outline="#ffffff", width=1)
        # reset edges
        for line_id in self.edge_items.values():
            self.canvas.itemconfig(line_id, fill="#9CA3AF", width=2)

    def get_start_node(self):
        txt = self.start_entry.get().strip()
        if not txt:
            return 1
        try:
            nid = int(txt)
            return nid
        except ValueError:
            return 1

    def animate_traversal(self, order, node_color="#f97316", edge_color="#f97316", delay_ms=500, done_text="Traversal done."):
        if not order:
            return

        self.reset_visual_style()

        def step(i):
            if i >= len(order):
                self.status_label.configure(text=done_text)
                return

            nid = order[i]
            self.highlight_node_fill(nid, node_color)

            if i > 0:
                u = order[i - 1]
                v = nid
                self.highlight_edge(u, v, edge_color, width=3)

            self.root.after(delay_ms, lambda: step(i + 1))

        step(0)

    # ------------------------------------------------------------------
    # Algorithm actions
    # ------------------------------------------------------------------
    def run_bfs(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty. Add persons first.")
            return
        start = self.get_start_node()
        try:
            order = bfs(self.graph, start)
        except Exception as e:
            self.status_label.configure(text=str(e))
            return
        self.status_label.configure(text=f"Running BFS from {start}...")
        self.animate_traversal(order, node_color="#f97316", edge_color="#f97316",
                               delay_ms=500, done_text="BFS finished.")

    def run_dfs(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty. Add persons first.")
            return
        start = self.get_start_node()
        try:
            order = dfs(self.graph, start)
        except Exception as e:
            self.status_label.configure(text=str(e))
            return
        self.status_label.configure(text=f"Running DFS from {start}...")
        self.animate_traversal(order, node_color="#3b82f6", edge_color="#3b82f6",
                               delay_ms=500, done_text="DFS finished.")

    def run_dijkstra(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty.")
            return
        start = self.get_start_node()
        target = max(self.graph.nodes.keys())
        dist, prev = dijkstra(self.graph, start)
        path = reconstruct_path(prev, start, target)
        if not path:
            self.status_label.configure(text=f"No path from {start} to {target}.")
            return
        self.reset_visual_style()
        self.status_label.configure(text=f"Showing Dijkstra shortest path {start} → {target}.")
        self.animate_traversal(path, node_color="#22c55e", edge_color="#22c55e",
                               delay_ms=600, done_text="Dijkstra path shown.")

    def run_astar(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty.")
            return
        start = self.get_start_node()
        target = max(self.graph.nodes.keys())
        dist, prev, path = astar(self.graph, start, target)
        if not path:
            self.status_label.configure(text=f"No path from {start} to {target}.")
            return
        self.reset_visual_style()
        self.status_label.configure(text=f"Showing A* shortest path {start} → {target}.")
        self.animate_traversal(path, node_color="#eab308", edge_color="#eab308",
                               delay_ms=600, done_text="A* path shown.")

    def run_components(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty.")
            return
        comps = connected_components(self.graph)
        self.reset_visual_style()

        colors = ["#22c55e", "#3b82f6", "#a855f7", "#ec4899", "#eab308"]
        for idx, comp in enumerate(comps):
            color = colors[idx % len(colors)]
            for nid in comp:
                self.highlight_node_fill(nid, color)
        self.status_label.configure(text=f"{len(comps)} connected component(s) highlighted.")

    def run_centrality(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty.")
            return
        results = degree_centrality(self.graph, top_n=5)
        important_nodes = [nid for nid, deg in results]
        self.reset_visual_style()
        for nid in important_nodes:
            self.highlight_node_fill(nid, "#f97316")
            self.highlight_node_border(nid, outline="#facc15", width=3)
        self.status_label.configure(
            text="Top central nodes: " + ", ".join(f"{nid}({deg})" for nid, deg in results)
        )

    def run_coloring(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty.")
            return
        coloring = welsh_powell(self.graph)
        self.reset_visual_style()
        palette = ["#22c55e", "#3b82f6", "#a855f7", "#ec4899", "#eab308", "#14b8a6"]
        for nid, color_idx in coloring.items():
            color = palette[color_idx % len(palette)]
            self.highlight_node_fill(nid, color)
        self.status_label.configure(text="Graph colored using Welsh–Powell algorithm.")


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    app = SocialNetworkUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
