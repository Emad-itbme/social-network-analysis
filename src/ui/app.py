import os
import sys
import math
import tkinter as tk
import customtkinter as ctk
import json
from tkinter import filedialog
import time



# -------------------------------------------------
# Add src/ to Python path
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
        self.node_items: dict[int, tuple[int, int]] = {}  # {id: (circle_item, text_item)}
        self.edge_items: dict[frozenset, int] = {}        # {frozenset({u,v}): line_item}
        self.next_node_id = 1
        self.selected_node = None

        # ----- main layout -----
        self.root.title("Social Network Analysis")
        self.root.geometry("1400x800")

        self.main_frame = ctk.CTkFrame(root, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        # Canvas (Left)
        self.canvas_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.canvas_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg="#15161E",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Sidebar (Right)
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

        # Bind events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Double-1>", self.on_node_info_click)


    # =================================================================
    # Right-click delete: node OR edge
    # =================================================================
    def on_right_click(self, event):
        x, y = event.x, event.y

        # Node deletion
        clicked_node = self.get_node_at(x, y)
        if clicked_node is not None:
            self.delete_node(clicked_node)
            return

        # Edge deletion
        clicked_edge = self.get_edge_at(x, y)
        if clicked_edge is not None:
            u, v = clicked_edge
            self.delete_edge(u, v)
            return


    def get_edge_at(self, x, y, tolerance=6):
        for key, line_id in self.edge_items.items():
            coords = self.canvas.coords(line_id)
            if len(coords) != 4:
                continue

            x1, y1, x2, y2 = coords
            dist = self.point_line_distance(x, y, x1, y1, x2, y2)
            if dist <= tolerance:
                return tuple(key)
        return None


    def point_line_distance(self, px, py, x1, y1, x2, y2):
        A = px - x1
        B = py - y1
        C = x2 - x1
        D = y2 - y1

        dot = A*C + B*D
        len_sq = C*C + D*D
        param = dot / len_sq if len_sq != 0 else -1

        if param < 0:
            xx, yy = x1, y1
        elif param > 1:
            xx, yy = x2, y2
        else:
            xx = x1 + param*C
            yy = y1 + param*D

        dx = px - xx
        dy = py - yy
        return math.sqrt(dx*dx + dy*dy)


    # =================================================================
    # DELETE NODE / DELETE EDGE
    # =================================================================
    def delete_node(self, nid):

        if nid not in self.node_items:
            return

        circle, text = self.node_items[nid]
        self.canvas.delete(circle)
        self.canvas.delete(text)

        # Delete edges touching node
        to_delete = [key for key in self.edge_items if nid in key]

        for key in to_delete:
            line = self.edge_items[key]
            self.canvas.delete(line)
            del self.edge_items[key]

            # backend remove
            for e in list(self.graph.edges):
                if (e.u in key and e.v in key):
                    self.graph.edges.remove(e)

        # backend node removal
        if nid in self.graph.nodes:
            del self.graph.nodes[nid]

        del self.node_positions[nid]
        del self.node_items[nid]

        if self.selected_node == nid:
            self.selected_node = None

        self.status_label.configure(text=f"Deleted person {nid}.")

    def delete_edge(self, u, v):
      key = frozenset({u, v})

      # 1) Remove from canvas
      if key in self.edge_items:
          self.canvas.delete(self.edge_items[key])
          del self.edge_items[key]

      # 2) Remove from graph backend (supports Edge or tuple)
      cleaned = []
      for e in self.graph.edges:
          if hasattr(e, "u") and hasattr(e, "v"):
              # Edge object
              if not ((e.u == u and e.v == v) or (e.u == v and e.v == u)):
                  cleaned.append(e)
          else:
              # tuple fallback
              eu, ev = e
              if not ((eu == u and ev == v) or (eu == v and ev == u)):
                  cleaned.append(e)

      self.graph.edges = cleaned

      self.status_label.configure(text=f"Deleted connection between {u} and {v}.")
    def show_text_popup(self, title, content):
        popup = ctk.CTkToplevel(self.root)
        popup.title(title)
        popup.geometry("500x600")
        popup.grab_set()

        text_box = ctk.CTkTextbox(popup, wrap="none")
        text_box.pack(fill="both", expand=True, padx=10, pady=10)

        text_box.insert("1.0", content)
        text_box.configure(state="disabled")
    def export_adjacency_list(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty.")
            return

        # Create adjacency list text
        lines = []
        for nid in sorted(self.graph.nodes.keys()):
            neighbors = sorted(self.graph.get_neighbors(nid))
            line = f"{nid}: {', '.join(map(str, neighbors)) or 'None'}"
            lines.append(line)

        content = "\n".join(lines)

        # Ask the user what they want to do
        choice = self.ask_export_action("Adjacency List")

        if choice == "show":
            self.show_text_popup("Adjacency List", content)
        elif choice == "save":
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save adjacency list"
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.status_label.configure(text=f"Adjacency list saved to {file_path}")
        else:
            # Cancel
            self.status_label.configure(text="Action cancelled.")
    def export_adjacency_matrix(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty.")
            return

        node_ids = sorted(self.graph.nodes.keys())

        matrix = []
        header = "    " + " ".join(f"{i:>3}" for i in node_ids)
        matrix.append(header)

        for i in node_ids:
            row = [f"{i:>3}"]
            for j in node_ids:
                if i == j:
                    val = 0
                else:
                    val = 1 if self.graph.has_edge(i, j) else 0
                row.append(f"{val:>3}")
            matrix.append(" ".join(row))

        content = "\n".join(matrix)

        # Ask user action
        choice = self.ask_export_action("Adjacency Matrix")

        if choice == "show":
            self.show_text_popup("Adjacency Matrix", content)

        elif choice == "save":
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save adjacency matrix"
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.status_label.configure(text=f"Adjacency matrix saved to {file_path}")

        else:
            self.status_label.configure(text="Action cancelled.")
    def ask_export_action(self, title="Select Action"):
        popup = ctk.CTkToplevel(self.root)
        popup.title(title)
        popup.geometry("300x150")
        popup.grab_set()

        label = ctk.CTkLabel(
            popup,
            text="Choose an action:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(pady=15)

        action = {"choice": None}

        def choose_show():
            action["choice"] = "show"
            popup.destroy()

        def choose_save():
            action["choice"] = "save"
            popup.destroy()

        def choose_cancel():
            action["choice"] = "cancel"
            popup.destroy()

        btn_frame = ctk.CTkFrame(popup)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Show", width=70, command=choose_show).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Save", width=70, command=choose_save).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancel", width=70, command=choose_cancel).pack(side="left", padx=5)

        popup.wait_window()
        return action["choice"]
    def measure_time(self, func, *args):
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        return result, (end - start)
    def run_performance_test(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty.")
            return

        results = {}

        start_node = min(self.graph.nodes.keys())
        end_node = max(self.graph.nodes.keys())

        # BFS
        _, t_bfs = self.measure_time(bfs, self.graph, start_node)
        results["BFS"] = t_bfs

        # DFS
        _, t_dfs = self.measure_time(dfs, self.graph, start_node)
        results["DFS"] = t_dfs

        # Dijkstra
        (_, _prev), t_dijkstra = self.measure_time(dijkstra, self.graph, start_node)
        results["Dijkstra"] = t_dijkstra

        # A*
        (_, _prev, _), t_astar = self.measure_time(astar, self.graph, start_node, end_node)
        results["A*"] = t_astar

        # Components
        _, t_components = self.measure_time(connected_components, self.graph)
        results["Connected Components"] = t_components

        # Coloring
        _, t_color = self.measure_time(welsh_powell, self.graph)
        results["Graph Coloring"] = t_color

        # Format report
        report_lines = ["Performance Report (seconds):\n"]
        for key, value in results.items():
            report_lines.append(f"{key:<22} : {value:.6f}")

        report = "\n".join(report_lines)

        # Show popup
        self.show_text_popup("Performance Report", report)

        # Ask if user wants to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save performance report"
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(report)
            self.status_label.configure(text="Performance report saved.")

    # =================================================================
    # Sidebar
    # =================================================================
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

        ctk.CTkButton(self.sidebar, text="BFS", command=self.run_bfs, **btn_cfg).pack(pady=4, padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="DFS", command=self.run_dfs, **btn_cfg).pack(pady=4, padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Dijkstra", command=self.run_dijkstra, **btn_cfg).pack(pady=4, padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="A*", command=self.run_astar, **btn_cfg).pack(pady=4, padx=10, fill="x")

        ctk.CTkButton(self.sidebar, text="Components", command=self.run_components, **btn_cfg).pack(pady=(12, 4), padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Centrality", command=self.run_centrality, **btn_cfg).pack(pady=4, padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Graph Coloring", command=self.run_coloring, **btn_cfg).pack(pady=4, padx=10, fill="x")

        ctk.CTkLabel(self.sidebar, text=" ", height=10).pack()

        ctk.CTkButton(
                  self.sidebar,
                  text="Adjacency List",
                  command=self.export_adjacency_list,
                  **btn_cfg
                 ).pack(pady=4, padx=10, fill="x")

        ctk.CTkButton(
                self.sidebar,
                text="Adjacency Matrix",
                command=self.export_adjacency_matrix,
                **btn_cfg
              ).pack(pady=4, padx=10, fill="x")
        
        ctk.CTkLabel(self.sidebar, text=" ", height=10).pack()
        ctk.CTkButton(
                   self.sidebar,
                   text="Load sample CSV",
                   command=self.load_sample_graph,
                   **btn_cfg
                ).pack(pady=4, padx=10, fill="x")

        ctk.CTkButton(
                    self.sidebar,
                    text="Save as JSON",
                    command=self.save_graph_to_json,
                    **btn_cfg
                 ).pack(pady=4, padx=10, fill="x")

        ctk.CTkButton(
                   self.sidebar,
                   text="Load from JSON",
                   command=self.load_graph_from_json,
                   **btn_cfg
                 ).pack(pady=4, padx=10, fill="x")
        ctk.CTkLabel(self.sidebar, text=" ", height=10).pack()
        ctk.CTkButton(
                self.sidebar,
                text="Performance Test",
                fg_color="#32a85f",
                 hover_color="#207a4d",
                command=self.run_performance_test,
                **btn_cfg
               ).pack(pady=1, padx=10, fill="x")

        ctk.CTkButton(
                 self.sidebar,
                 text="Clear graph",
                 fg_color="#a83232",
                 hover_color="#7a2020",
                 command=self.clear_graph,
                 **btn_cfg
                ).pack(pady=(8, 4), padx=10, fill="x")



    # =================================================================
    # Canvas interactions: left click
    # =================================================================
    def on_canvas_click(self, event):
        x, y = event.x, event.y
        clicked_id = self.get_node_at(x, y)

        if clicked_id is None:
            self.open_node_popup(x, y)
            return

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
            self.highlight_node_border(self.selected_node, outline="#ffffff", width=1)
            self.selected_node = None
    def on_node_info_click(self, event):
        """Open info popup when user double-clicks on a node."""
        x, y = event.x, event.y
        nid = self.get_node_at(x, y)
        if nid is None:
            return  # double-click on empty area, ignore
        self.open_node_info_popup(nid)


    def get_node_at(self, x, y):
        for nid, (circle, _) in self.node_items.items():
            cx, cy = self.node_positions[nid]
            if (x - cx)**2 + (y - cy)**2 <= self.node_radius**2:
                return nid
        return None


    # =================================================================
    # Node creation popup
    # =================================================================
    def open_node_popup(self, x, y):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Add Person")
        popup.geometry("300x260")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Create new person",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        name_entry = ctk.CTkEntry(popup, placeholder_text="Name")
        name_entry.pack(pady=4, padx=20, fill="x")

        act_entry = ctk.CTkEntry(popup, placeholder_text="Activity (0-1)")
        act_entry.pack(pady=4, padx=20, fill="x")

        inter_entry = ctk.CTkEntry(popup, placeholder_text="Interaction")
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
                error_label.configure(text="Enter numeric values for activity/interaction/connections.")
                return

            popup.destroy()
            self.create_node(x, y, name, activity, interaction, conn_count)

        btn_frame = ctk.CTkFrame(popup)
        btn_frame.pack(pady=10, fill="x")

        ctk.CTkButton(btn_frame, text="Cancel", command=popup.destroy).pack(side="left", padx=10, expand=True)
        ctk.CTkButton(btn_frame, text="Create", command=on_confirm).pack(side="right", padx=10, expand=True)
    def open_node_info_popup(self, nid: int):
        """Show detailed information about a person (node)."""

        if nid not in self.graph.nodes:
            return

        node = self.graph.nodes[nid]
        neighbors = sorted(self.graph.get_neighbors(nid))
        degree = len(neighbors)

        popup = ctk.CTkToplevel(self.root)
        popup.title(f"Person {nid} info")
        popup.geometry("340x360")
        popup.grab_set()

        title_label = ctk.CTkLabel(
            popup,
            text=f"Person ID: {nid}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(10, 5))

        # Name
        name_label = ctk.CTkLabel(popup, text="Name:")
        name_label.pack(anchor="w", padx=20)
        name_entry = ctk.CTkEntry(popup)
        name_entry.insert(0, node.name or f"User {nid}")
        name_entry.pack(pady=(0, 8), padx=20, fill="x")

        # Activity
        act_label = ctk.CTkLabel(popup, text="Activity (0-1):")
        act_label.pack(anchor="w", padx=20)
        act_entry = ctk.CTkEntry(popup)
        act_entry.insert(0, str(node.activity))
        act_entry.pack(pady=(0, 8), padx=20, fill="x")

        # Interaction
        inter_label = ctk.CTkLabel(popup, text="Interaction:")
        inter_label.pack(anchor="w", padx=20)
        inter_entry = ctk.CTkEntry(popup)
        inter_entry.insert(0, str(node.interaction))
        inter_entry.pack(pady=(0, 8), padx=20, fill="x")

        # Connection count
        conn_label = ctk.CTkLabel(popup, text="Connection count:")
        conn_label.pack(anchor="w", padx=20)
        conn_entry = ctk.CTkEntry(popup)
        conn_entry.insert(0, str(node.connection_count))
        conn_entry.pack(pady=(0, 8), padx=20, fill="x")

        # Degree + neighbors (read-only)
        degree_label = ctk.CTkLabel(
            popup,
            text=f"Degree: {degree}   Neighbors: {', '.join(map(str, neighbors)) or 'None'}",
            wraplength=300,
            justify="left"
        )
        degree_label.pack(pady=(8, 4), padx=20)

        error_label = ctk.CTkLabel(popup, text="", text_color="red")
        error_label.pack(pady=(2, 4))

        def on_save():
            """Update node attributes from the form."""
            try:
                new_name = name_entry.get().strip() or f"User {nid}"
                new_activity = float(act_entry.get())
                new_interaction = float(inter_entry.get())
                new_conn = float(conn_entry.get())
            except ValueError:
                error_label.configure(text="Please enter valid numeric values.")
                return

            # Update backend node
            self.graph.update_node(
                nid,
                name=new_name,
                activity=new_activity,
                interaction=int(new_interaction),
                connection_count=int(new_conn),
            )

            # Optionally update status bar
            self.status_label.configure(
                text=f"Updated person {nid}: {new_name}, activity={new_activity}"
            )

            popup.destroy()

        def on_delete():
            """Delete the node from graph and UI."""
            popup.destroy()
            self.delete_node(nid)

        btn_frame = ctk.CTkFrame(popup)
        btn_frame.pack(pady=10, fill="x")

        delete_btn = ctk.CTkButton(
            btn_frame,
            text="Delete",
            fg_color="#a83232",
            hover_color="#7a2020",
            command=on_delete
        )
        delete_btn.pack(side="left", padx=10, expand=True)

        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save",
            command=on_save
        )
        save_btn.pack(side="right", padx=10, expand=True)


    # =================================================================
    # Create node + draw on canvas
    # =================================================================
    def create_node(self, x, y, name, activity, interaction, connection_count):
        nid = self.next_node_id
        self.next_node_id += 1

        self.graph.add_node(
            nid,
            name=name,
            activity=activity,
            interaction=interaction,
            connection_count=connection_count
        )

        circle = self.canvas.create_oval(
            x - self.node_radius, y - self.node_radius,
            x + self.node_radius, y + self.node_radius,
            fill="#3A5166",
            outline="#ffffff",
            width=1
        )

        text = self.canvas.create_text(
            x, y, text=str(nid),
            fill="#e5e7eb",
            font=("Segoe UI", 12, "bold")
        )

        self.node_positions[nid] = (x, y)
        self.node_items[nid] = (circle, text)

        self.status_label.configure(text=f"Person {nid} created.")


    # =================================================================
    # Edge creation
    # =================================================================
    def highlight_node_border(self, nid, outline="#ffffff", width=1):
        circle, _ = self.node_items[nid]
        self.canvas.itemconfig(circle, outline=outline, width=width)


    def highlight_node_fill(self, nid, color):
        circle, _ = self.node_items[nid]
        self.canvas.itemconfig(circle, fill=color)


    def highlight_edge(self, u, v, color, width=3):
        key = frozenset({u, v})
        line_id = self.edge_items.get(key)
        if line_id:
            self.canvas.itemconfig(line_id, fill=color, width=width)


    def create_edge(self, u, v):
        if u == v:
            return

        key = frozenset({u, v})
        if key in self.edge_items:
            return

        x1, y1 = self.node_positions[u]
        x2, y2 = self.node_positions[v]

        line_id = self.canvas.create_line(x1, y1, x2, y2, fill="#9CA3AF", width=2)
        self.edge_items[key] = line_id

        n1 = self.graph.nodes[u]
        n2 = self.graph.nodes[v]

        weight = 1.0 / (
            1.0 + math.sqrt(
                (n1.activity - n2.activity)**2 +
                (n1.interaction - n2.interaction)**2 +
                (n1.connection_count - n2.connection_count)**2
            )
        )

        self.graph.add_edge(u, v, weight)


    # =================================================================
    # Graph reset / load
    # =================================================================
    def clear_graph(self):
        self.canvas.delete("all")
        self.graph = Graph()

        self.node_positions.clear()
        self.node_items.clear()
        self.edge_items.clear()

        self.next_node_id = 1
        self.selected_node = None

        self.status_label.configure(text="Graph cleared.")
    def save_graph_to_json(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty. Nothing to save.")
            return

        file_path = filedialog.asksaveasfilename(

            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Save graph as JSON"
        )
        if not file_path:
            return

        data = {"nodes": [], "edges": []}

        # Serialize nodes with positions
        for nid, node in self.graph.nodes.items():
            x, y = self.node_positions.get(nid, (0.0, 0.0))
            data["nodes"].append({
                "id": nid,
                "name": node.name,
                "activity": node.activity,
                "interaction": node.interaction,
                "connection_count": node.connection_count,
                "x": x,
                "y": y,
            })

        # Serialize edges
        for edge in self.graph.get_edges():
            data["edges"].append({
                "u": edge.u,
                "v": edge.v,
                "weight": edge.weight,
            })

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.status_label.configure(text=f"Graph saved to {os.path.basename(file_path)}.")
        except Exception as e:
            self.status_label.configure(text=f"Failed to save JSON: {e}")
    def load_graph_from_json(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Load graph from JSON"
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            self.status_label.configure(text=f"Failed to read JSON: {e}")
            return

        # Reset current graph and visuals
        self.canvas.delete("all")
        from models.graph import Graph
        self.graph = Graph()
        self.node_positions.clear()
        self.node_items.clear()
        self.edge_items.clear()
        self.selected_node = None

        # Rebuild nodes
        for node_data in data.get("nodes", []):
            nid = int(node_data["id"])
            name = node_data.get("name")
            activity = float(node_data.get("activity", 0.0))
            interaction = int(node_data.get("interaction", 0))
            connection_count = int(node_data.get("connection_count", 0))

            # Add to backend graph
            self.graph.add_node(
                nid,
                name=name,
                activity=activity,
                interaction=interaction,
                connection_count=connection_count,
            )

            # Draw on canvas
            x = float(node_data.get("x", 0.0))
            y = float(node_data.get("y", 0.0))

            circle = self.canvas.create_oval(
                x - self.node_radius, y - self.node_radius,
                x + self.node_radius, y + self.node_radius,
                fill="#3A5166",
                outline="#ffffff",
                width=1
            )
            text = self.canvas.create_text(
                x, y, text=str(nid),
                fill="#e5e7eb",
                font=("Segoe UI", 12, "bold")
            )

            self.node_positions[nid] = (x, y)
            self.node_items[nid] = (circle, text)

        # Rebuild edges
        for e_data in data.get("edges", []):
            u = int(e_data.get("u"))
            v = int(e_data.get("v"))
            weight = float(e_data.get("weight", 1.0))

            if u not in self.graph.nodes or v not in self.graph.nodes:
                continue

            # Backend edge
            self.graph.add_edge(u, v, weight)

            # Visual edge
            x1, y1 = self.node_positions[u]
            x2, y2 = self.node_positions[v]
            line_id = self.canvas.create_line(x1, y1, x2, y2, fill="#9CA3AF", width=2)
            self.edge_items[frozenset({u, v})] = line_id

        # Update next_node_id for adding new nodes later
        if self.graph.nodes:
            self.next_node_id = max(self.graph.nodes.keys()) + 1
        else:
            self.next_node_id = 1

        self.status_label.configure(text=f"Graph loaded from {os.path.basename(file_path)}.")


    
    # =================================================================
    # Animation helpers
    # =================================================================
    def reset_visual_style(self):
        for nid in self.node_items:
            self.highlight_node_fill(nid, "#3A5166")
            self.highlight_node_border(nid, outline="#ffffff", width=1)
        for line_id in self.edge_items.values():
            self.canvas.itemconfig(line_id, fill="#9CA3AF", width=2)


    def get_start_node(self):
        txt = self.start_entry.get().strip()
        if not txt:
            return 1
        try:
            return int(txt)
        except ValueError:
            return 1


    def animate_traversal(self, order, node_color="#f97316",
                          edge_color="#f97316", delay_ms=500,
                          done_text="Traversal done."):

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
                u = order[i-1]
                v = order[i]
                self.highlight_edge(u, v, edge_color, width=3)

            self.root.after(delay_ms, lambda: step(i+1))

        step(0)
    def load_sample_graph(self):
     print(">>> LOAD SAMPLE GRAPH")
     print("FILE:", __file__)

     # Determine the project root
     ui_dir = os.path.dirname(os.path.abspath(__file__))
     src_dir = os.path.dirname(ui_dir)
     project_root = os.path.dirname(src_dir)

     csv_path = os.path.join(project_root, "data", "sample_small.csv")
     print("CSV PATH:", csv_path)

     if not os.path.exists(csv_path):
         print("CSV NOT FOUND:", csv_path)
         self.status_label.configure(text="ERROR: CSV not found.")
         return

     from models.graph_loader import GraphLoader

     # Reset UI
     self.canvas.delete("all")
     self.node_positions.clear()
     self.node_items.clear()
     self.edge_items.clear()
     self.selected_node = None

     # Load Backend Graph
     self.graph = GraphLoader.load_from_csv(csv_path)

     # Layout nodes in a circle
     width = self.canvas.winfo_width() or 900
     height = self.canvas.winfo_height() or 700
     cx, cy = width // 2, height // 2
     radius = min(width, height) // 2 - 120

     node_ids = sorted(self.graph.nodes.keys())
     n = len(node_ids) if node_ids else 1

     # Draw nodes
     for i, nid in enumerate(node_ids):
         angle = 2 * math.pi * i / n
         x = cx + radius * math.cos(angle)
         y = cy + radius * math.sin(angle)

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

     # Draw edges — FIXED VERSION
     for edge in self.graph.get_edges():  # <<< THIS WAS THE BUG
         u, v = edge.u, edge.v
         x1, y1 = self.node_positions[u]
         x2, y2 = self.node_positions[v]
         line_id = self.canvas.create_line(
             x1, y1, x2, y2, fill="#9CA3AF", width=2
         )
         self.edge_items[frozenset({u, v})] = line_id

     # Fix next node ID
     if self.graph.nodes:
         self.next_node_id = max(self.graph.nodes.keys()) + 1
     else:
         self.next_node_id = 1

     self.status_label.configure(text="Sample CSV loaded successfully.")


    # =================================================================
    # Algorithm actions
    # =================================================================
    def run_bfs(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty.")
            return

        start = self.get_start_node()
        try:
            order = bfs(self.graph, start)
        except Exception as e:
            self.status_label.configure(text=str(e))
            return

        self.status_label.configure(text=f"BFS from {start}...")
        self.animate_traversal(order, node_color="#f97316", edge_color="#f97316")


    def run_dfs(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty.")
            return

        start = self.get_start_node()
        try:
            order = dfs(self.graph, start)
        except Exception as e:
            self.status_label.configure(text=str(e))
            return

        self.status_label.configure(text=f"DFS from {start}...")
        self.animate_traversal(order, node_color="#3b82f6", edge_color="#3b82f6")


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
        self.status_label.configure(text=f"Dijkstra path {start}->{target}")
        self.animate_traversal(path, node_color="#22c55e", edge_color="#22c55e")


    def run_astar(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty.")
            return

        start = self.get_start_node()
        target = max(self.graph.nodes.keys())

        dist, prev, path = astar(self.graph, start, target)
        if not path:
            self.status_label.configure(text="No A* path.")
            return

        self.reset_visual_style()
        self.status_label.configure(text=f"A* path {start}->{target}")
        self.animate_traversal(path, node_color="#eab308", edge_color="#eab308")


    def run_components(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty.")
            return

        comps = connected_components(self.graph)

        self.reset_visual_style()

        palette = ["#22c55e", "#3b82f6", "#a855f7", "#ec4899", "#eab308"]

        for i, comp in enumerate(comps):
            color = palette[i % len(palette)]
            for nid in comp:
                self.highlight_node_fill(nid, color)

        self.status_label.configure(text=f"{len(comps)} component(s).")


    def run_centrality(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty.")
            return

        results = degree_centrality(self.graph, 5)
        important = [nid for nid, deg in results]

        self.reset_visual_style()

        for nid in important:
            self.highlight_node_fill(nid, "#f97316")
            self.highlight_node_border(nid, outline="#facc15", width=3)

        txt = ", ".join(f"{nid}({deg})" for nid, deg in results)
        self.status_label.configure(text="Central nodes: " + txt)


    def run_coloring(self):
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty.")
            return

        coloring = welsh_powell(self.graph)
        palette = ["#22c55e", "#3b82f6", "#a855f7", "#ec4899", "#eab308", "#14b8a6"]

        self.reset_visual_style()

        for nid, color_idx in coloring.items():
            self.highlight_node_fill(nid, palette[color_idx % len(palette)])

        self.status_label.configure(text="Graph colored.")



# =====================================================================
# MAIN
# =====================================================================
def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    app = SocialNetworkUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
