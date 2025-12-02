import os
import sys
import math
import tkinter as tk
import customtkinter as ctk
import json
from tkinter import filedialog, messagebox
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# -------------------------------------------------
# Configure logging
# -------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# -------------------------------------------------
# Notification & UI Constants
# -------------------------------------------------
@dataclass
class Notification:
    message: str
    duration_ms: int = 3000
    notification_type: str = "info"  # "info", "success", "warning", "error"

class NotificationType(Enum):
    INFO = ("#3b82f6", "ℹ")
    SUCCESS = ("#22c55e", "✓")
    WARNING = ("#f97316", "⚠")
    ERROR = ("#ef4444", "✕")

# -------------------------------------------------
# Add src/ to Python path
# -------------------------------------------------
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from models.graph import Graph
from models.graph_loader import GraphLoader
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
        self.node_categories: dict[int, str] = {}         # {id: category}
        self.category_colors = {
            "default": "#3A5166",
            "influencer": "#f97316",
            "group": "#3b82f6",
            "moderate": "#22c55e",
            "inactive": "#6b7280"
        }
        self.next_node_id = 1
        self.selected_node = None
        self.is_processing = False
        self.notification_queue: List[Notification] = []
        
        # ----- History/Undo system -----
        self.history: List[Dict] = []
        self.history_index = -1
        self.max_history = 50
        
        # ----- Drag and drop -----
        self.dragging_node = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # ----- Canvas zoom/pan -----
        self.canvas_scale = 1.0
        self.pan_x = 0
        self.pan_y = 0
        
        # ----- Last algorithm result -----
        self.last_algorithm_result = None
        self.last_algorithm_name = ""
        
        # ----- Hover & Animation -----
        self.hovered_node = None
        self.tooltip_id = None
        self.hover_timer = None
        self.algorithm_animation_speed = 100  # ms between steps
        self.node_glow_effect = {}  # Store glow radius for animation
        self.algorithm_colors = []
        self.gradient_map = {}  # Maps node ID to gradient color

        # ----- main layout -----
        self.root.title("Social Network Analysis")
        self.root.geometry("1600x900")

        self.main_frame = ctk.CTkFrame(root, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        # Top Header Bar
        self.build_header_bar()

        # Content frame (canvas + sidebar)
        self.content_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        self.content_frame.pack(fill="both", expand=True)

        # Canvas (Left)
        self.canvas_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        self.canvas_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Stats panel (above canvas)
        self.build_stats_panel()

        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg="#15161E",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Sidebar (Right)
        self.sidebar = ctk.CTkFrame(self.content_frame, corner_radius=10, width=280)
        self.sidebar.pack(side="right", fill="y", padx=10, pady=10)

        self.build_sidebar()

        # Status bar + Notification area
        self.build_footer()

        # Bind events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Double-1>", self.on_node_info_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<MouseWheel>", self.on_canvas_scroll)
        self.canvas.bind("<Button-4>", self.on_canvas_scroll)  # Linux scroll up
        self.canvas.bind("<Button-5>", self.on_canvas_scroll)  # Linux scroll down
        self.root.bind("<Delete>", self.on_delete_key)
        self.root.bind("<Control-z>", self.on_undo_key)
        self.root.bind("<Control-f>", self.on_search_key)
        self.root.bind("<Control-y>", self.on_redo_key)
        self.canvas.bind("<Motion>", self.on_canvas_hover)


    # =================================================================
    # Header Bar with Title and Quick Stats
    # =================================================================
    def build_header_bar(self):
        """Create a professional header bar with app title and quick actions."""
        header = ctk.CTkFrame(self.main_frame, height=70, fg_color="#0f0f12", corner_radius=0)
        header.pack(fill="x", side="top", pady=0)
        header.pack_propagate(False)

        # Left section: Title
        left_section = ctk.CTkFrame(header, fg_color="transparent")
        left_section.pack(side="left", padx=20, pady=15)

        title = ctk.CTkLabel(
            left_section,
            text="🌐 Social Network Analysis",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        title.pack(side="left")

        # Center section: Quick stats
        self.stats_frame = ctk.CTkFrame(header, fg_color="transparent")
        self.stats_frame.pack(side="left", padx=30, pady=15, expand=True)

        # Right section: Help
        right_section = ctk.CTkFrame(header, fg_color="transparent")
        right_section.pack(side="right", padx=20, pady=15)

        help_btn = ctk.CTkButton(
            right_section,
            text="?",
            width=40,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.show_help,
            fg_color="#2d2d35",
            hover_color="#3d3d45"
        )
        help_btn.pack(side="left", padx=5)

    # =================================================================
    # Statistics Panel
    # =================================================================
    def build_stats_panel(self):
        """Create a stats panel showing graph information."""
        self.stats_panel = ctk.CTkFrame(self.canvas_frame, fg_color="#1a1a22", corner_radius=8, height=80)
        self.stats_panel.pack(fill="x", padx=0, pady=(0, 8))
        self.stats_panel.pack_propagate(False)

        # Top row: stats
        stats_row = ctk.CTkFrame(self.stats_panel, fg_color="transparent")
        stats_row.pack(fill="x", padx=15, pady=(10, 0))

        self.nodes_label = ctk.CTkLabel(stats_row, text="Nodes: 0", font=ctk.CTkFont(size=13, weight="bold"))
        self.nodes_label.pack(side="left", padx=15)

        self.edges_label = ctk.CTkLabel(stats_row, text="Edges: 0", font=ctk.CTkFont(size=13, weight="bold"))
        self.edges_label.pack(side="left", padx=15)

        self.density_label = ctk.CTkLabel(stats_row, text="Density: 0.00", font=ctk.CTkFont(size=13, weight="bold"))
        self.density_label.pack(side="left", padx=15)

        # Bottom row: category legend
        legend_row = ctk.CTkFrame(self.stats_panel, fg_color="transparent")
        legend_row.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkLabel(legend_row, text="Categories:", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=(0, 15))
        
        for cat, color in self.category_colors.items():
            if cat != "default":
                dot = ctk.CTkLabel(legend_row, text="●", text_color=color, font=ctk.CTkFont(size=12))
                dot.pack(side="left", padx=2)
                label = ctk.CTkLabel(legend_row, text=cat.capitalize(), font=ctk.CTkFont(size=11))
                label.pack(side="left", padx=5)

    def update_stats(self):
        """Update graph statistics display."""
        n = len(self.graph.nodes)
        e = len(self.graph.edges)
        density = (2 * e) / (n * (n - 1)) if n > 1 else 0.0

        self.nodes_label.configure(text=f"Nodes: {n}")
        self.edges_label.configure(text=f"Edges: {e}")
        self.density_label.configure(text=f"Density: {density:.3f}")

    # =================================================================
    # Footer with Status and Notifications
    # =================================================================
    def build_footer(self):
        """Create footer with status bar and notification area."""
        footer = ctk.CTkFrame(self.root, fg_color="#0f0f12", height=80, corner_radius=0)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        # Status label
        self.status_label = ctk.CTkLabel(
            footer,
            text="Ready. Click on canvas to add a person.",
            anchor="w",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.status_label.pack(fill="x", padx=15, pady=(10, 5))

        # Notification area
        self.notification_label = ctk.CTkLabel(
            footer,
            text="",
            anchor="w",
            font=ctk.CTkFont(size=12)
        )
        self.notification_label.pack(fill="x", padx=15, pady=(0, 10))

    def show_notification(self, message: str, notification_type: str = "info", duration_ms: int = 3000):
        """Show a notification message."""
        notif_type_map = {
            "info": NotificationType.INFO,
            "success": NotificationType.SUCCESS,
            "warning": NotificationType.WARNING,
            "error": NotificationType.ERROR,
        }
        notif_type = notif_type_map.get(notification_type, NotificationType.INFO)
        color, icon = notif_type.value

        display_text = f"{icon} {message}"
        self.notification_label.configure(text=display_text, text_color=color)

        # Auto-clear after duration
        self.root.after(duration_ms, lambda: self.notification_label.configure(text=""))

    # =================================================================
    # Help Dialog
    # =================================================================
    def show_help(self):
        """Show help dialog with keyboard shortcuts."""
        popup = ctk.CTkToplevel(self.root)
        popup.title("Help & Shortcuts")
        popup.geometry("500x550")
        popup.grab_set()

        title = ctk.CTkLabel(
            popup,
            text="Keyboard Shortcuts & Help",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=15)

        shortcuts = [
            ("Left Click", "Add node or connect nodes"),
            ("Right Click", "Delete node or edge"),
            ("Double Click", "Edit node properties"),
            ("Delete", "Delete selected node"),
            ("Ctrl+F", "Search nodes"),
            ("Ctrl+Z", "Undo (reserved for future)"),
            ("", ""),
            ("Canvas", "Graph visualization area"),
            ("Sidebar", "Algorithm controls & exports"),
            ("Stats", "Real-time graph statistics"),
        ]

        text_box = ctk.CTkTextbox(popup, wrap="word", height=20)
        text_box.pack(fill="both", expand=True, padx=15, pady=10)

        for key, desc in shortcuts:
            if key:
                text_box.insert("end", f"{key:<15} → {desc}\n")
            else:
                text_box.insert("end", "\n")

        text_box.configure(state="disabled")

        ctk.CTkButton(popup, text="Close", command=popup.destroy).pack(pady=10)

    # =================================================================
    # Keyboard Shortcuts
    # =================================================================
    def on_delete_key(self, event):
        """Delete selected node with Delete key."""
        if self.selected_node is not None:
            self.delete_node(self.selected_node)
            self.show_notification(f"Node {self.selected_node} deleted", "success", 2000)
            self.selected_node = None

    def on_undo_key(self, event):
        """Undo action (placeholder for future implementation)."""
        self.show_notification("Undo feature coming soon", "info", 2000)

    def on_redo_key(self, event):
        """Redo action (placeholder for future implementation)."""
        self.show_notification("Redo feature coming soon", "info", 2000)

    def on_search_key(self, event):
        """Open search dialog."""
        self.show_search_dialog()

    def show_search_dialog(self):
        """Show search dialog for finding nodes."""
        popup = ctk.CTkToplevel(self.root)
        popup.title("Search Nodes")
        popup.geometry("350x200")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Search by ID or Name:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=10)

        search_entry = ctk.CTkEntry(popup, placeholder_text="Enter node ID or name")
        search_entry.pack(pady=5, padx=20, fill="x")

        results_label = ctk.CTkLabel(popup, text="", justify="left")
        results_label.pack(pady=10, padx=20, fill="both")

        def search():
            query = search_entry.get().strip().lower()
            if not query:
                results_label.configure(text="Enter search term")
                return

            matches = []
            for nid, node in self.graph.nodes.items():
                if query.isdigit() and str(nid) == query:
                    matches.append(f"ID {nid}: {node.name or f'User {nid}'}")
                elif query in (node.name or "").lower():
                    matches.append(f"ID {nid}: {node.name}")

            if matches:
                results_label.configure(text="\n".join(matches), text_color="#22c55e")
            else:
                results_label.configure(text="No results found", text_color="#ef4444")

        ctk.CTkButton(popup, text="Search", command=search).pack(pady=10)

    # =================================================================
    # Canvas Drag, Zoom, Pan Controls
    # =================================================================
    def on_canvas_drag(self, event):
        """Handle node dragging on canvas."""
        x, y = event.x, event.y
        
        if self.dragging_node is None:
            # Check if we're dragging a node
            dragging = self.get_node_at(x, y)
            if dragging is not None and self.selected_node is None:
                self.dragging_node = dragging
                self.drag_start_x = x
                self.drag_start_y = y
                self.show_notification(f"Dragging node {dragging}", "info", 1000)
        
        if self.dragging_node is not None:
            # Calculate movement
            dx = x - self.drag_start_x
            dy = y - self.drag_start_y
            
            # Update node position
            old_x, old_y = self.node_positions[self.dragging_node]
            new_x, new_y = old_x + dx, old_y + dy
            
            # Move node on canvas
            circle, text = self.node_items[self.dragging_node]
            self.canvas.coords(circle, 
                              new_x - self.node_radius, new_y - self.node_radius,
                              new_x + self.node_radius, new_y + self.node_radius)
            self.canvas.coords(text, new_x, new_y)
            
            # Update edges connected to this node
            for neighbor in self.graph.get_neighbors(self.dragging_node):
                key = frozenset({self.dragging_node, neighbor})
                if key in self.edge_items:
                    line_id = self.edge_items[key]
                    neighbor_x, neighbor_y = self.node_positions[neighbor]
                    self.canvas.coords(line_id, new_x, new_y, neighbor_x, neighbor_y)
            
            # Update internal position
            self.node_positions[self.dragging_node] = (new_x, new_y)
            self.drag_start_x = x
            self.drag_start_y = y

    def on_canvas_release(self, event):
        """Handle mouse release after dragging."""
        if self.dragging_node is not None:
            self.show_notification(f"Node {self.dragging_node} moved", "success", 1500)
            self.dragging_node = None

    def on_canvas_scroll(self, event):
        """Handle canvas zoom with mouse wheel."""
        # Determine zoom direction
        if event.num == 5 or event.delta < 0:
            # Scroll down = zoom out
            zoom_factor = 0.9
        else:
            # Scroll up = zoom in
            zoom_factor = 1.1
        
        # Update scale
        self.canvas_scale *= zoom_factor
        
        # Limit zoom levels
        if self.canvas_scale < 0.3:
            self.canvas_scale = 0.3
        elif self.canvas_scale > 3.0:
            self.canvas_scale = 3.0
        
        # Redraw everything with new scale
        self.redraw_canvas_with_zoom()
        zoom_percent = int(self.canvas_scale * 100)
        self.show_notification(f"Zoom: {zoom_percent}%", "info", 800)
    
    def on_canvas_hover(self, event):
        """Handle mouse hover for node tooltips."""
        x, y = event.x, event.y
        hovered = self.get_node_at(x, y)
        
        # Clear previous hover
        if self.hovered_node is not None and self.hovered_node != hovered:
            if self.hovered_node in self.node_items:
                circle, _ = self.node_items[self.hovered_node]
                # Restore original width
                category = self.node_categories.get(self.hovered_node, "default")
                color = self.category_colors.get(category, self.category_colors["default"])
                self.canvas.itemconfig(circle, outline="#ffffff", width=max(1, int(self.canvas_scale)))
        
        # Show hover effect on new node
        if hovered is not None and hovered != self.selected_node:
            if hovered in self.node_items:
                circle, _ = self.node_items[hovered]
                # Highlight on hover
                self.canvas.itemconfig(circle, outline="#fbbf24", width=max(3, int(3 * self.canvas_scale)))
        
        self.hovered_node = hovered
        
        # Cancel previous tooltip timer
        if self.hover_timer:
            self.root.after_cancel(self.hover_timer)
        
        # Show tooltip after 800ms hover
        if hovered is not None:
            self.hover_timer = self.root.after(800, lambda: self.show_node_tooltip(hovered, x, y))
        else:
            self.hide_node_tooltip()
    
    def show_node_tooltip(self, nid, x, y):
        """Show a tooltip with node information."""
        if nid not in self.graph.nodes:
            return
        
        node = self.graph.nodes[nid]
        neighbors = list(self.graph.get_neighbors(nid))
        degree = len(neighbors)
        category = self.node_categories.get(nid, "default")
        
        tooltip_text = f"ID: {nid}\n"
        tooltip_text += f"Name: {node.name or f'User {nid}'}\n"
        tooltip_text += f"Degree: {degree}\n"
        tooltip_text += f"Activity: {node.activity:.2f}\n"
        tooltip_text += f"Category: {category}"
        
        # Create tooltip window
        if self.tooltip_id:
            try:
                self.canvas.delete(self.tooltip_id)
            except:
                pass
        
        # Create a semi-transparent background for tooltip
        tooltip_id = self.canvas.create_text(
            x + 20, y - 30,
            text=tooltip_text,
            fill="#e5e7eb",
            font=("Segoe UI", 10, "bold"),
            anchor="nw",
            tags="tooltip"
        )
        self.tooltip_id = tooltip_id
    
    def hide_node_tooltip(self):
        """Hide the tooltip."""
        if self.tooltip_id:
            try:
                self.canvas.delete(self.tooltip_id)
            except:
                pass
            self.tooltip_id = None

    def redraw_canvas_with_zoom(self):
        """Redraw all canvas elements with current zoom scale."""
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            return
        
        # Store original positions if not already stored
        if not hasattr(self, 'original_positions'):
            self.original_positions = {nid: pos for nid, pos in self.node_positions.items()}
        
        # Clear and redraw edges first
        for key, line_id in list(self.edge_items.items()):
            self.canvas.delete(line_id)
        self.edge_items.clear()
        
        # Redraw edges with scaled positions
        for u, v in [(e.u, e.v) for e in self.graph.get_edges()]:
            if u in self.original_positions and v in self.original_positions:
                u_x, u_y = self.original_positions[u]
                v_x, v_y = self.original_positions[v]
                
                # Scale positions
                scaled_u_x = u_x * self.canvas_scale
                scaled_u_y = u_y * self.canvas_scale
                scaled_v_x = v_x * self.canvas_scale
                scaled_v_y = v_y * self.canvas_scale
                
                line_id = self.canvas.create_line(
                    scaled_u_x, scaled_u_y, scaled_v_x, scaled_v_y,
                    fill="#9CA3AF", width=max(1, int(2 * self.canvas_scale))
                )
                self.edge_items[frozenset({u, v})] = line_id
        
        # Redraw nodes with scaled radius
        scaled_radius = max(self.node_radius * self.canvas_scale, 6)
        
        for nid, (x, y) in self.original_positions.items():
            # Delete old items if they exist
            if nid in self.node_items:
                old_circle, old_text = self.node_items[nid]
                self.canvas.delete(old_circle)
                self.canvas.delete(old_text)
            
            # Scale positions
            scaled_x = x * self.canvas_scale
            scaled_y = y * self.canvas_scale
            
            # Get node category color
            category = self.node_categories.get(nid, "default")
            color = self.category_colors.get(category, self.category_colors["default"])
            
            # Create scaled circle
            circle = self.canvas.create_oval(
                scaled_x - scaled_radius, scaled_y - scaled_radius,
                scaled_x + scaled_radius, scaled_y + scaled_radius,
                fill=color,
                outline="#ffffff",
                width=max(1, int(self.canvas_scale))
            )
            
            # Create scaled text
            text = self.canvas.create_text(
                scaled_x, scaled_y, text=str(nid),
                fill="#e5e7eb",
                font=("Segoe UI", max(8, int(12 * self.canvas_scale)), "bold")
            )
            
            self.node_items[nid] = (circle, text)
            # Update display position
            self.node_positions[nid] = (scaled_x, scaled_y)

    def apply_zoom(self):
        """Apply zoom transformation to all nodes and edges."""
        # Get canvas center
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            return
        
        center_x = canvas_width / 2
        center_y = canvas_height / 2
        
        # Update all node positions based on zoom
        for nid, (old_x, old_y) in list(self.node_positions.items()):
            # Scale relative to center
            new_x = center_x + (old_x - center_x) * (self.canvas_scale / (self.canvas_scale / 1.15 if self.canvas_scale > 1 else self.canvas_scale * 1.15))
            new_y = center_y + (old_y - center_y) * (self.canvas_scale / (self.canvas_scale / 1.15 if self.canvas_scale > 1 else self.canvas_scale * 1.15))
            
            # Update node on canvas
            if nid in self.node_items:
                circle, text = self.node_items[nid]
                scaled_radius = max(self.node_radius * self.canvas_scale, 8)
                
                self.canvas.coords(circle,
                                  new_x - scaled_radius, new_y - scaled_radius,
                                  new_x + scaled_radius, new_y + scaled_radius)
                self.canvas.coords(text, new_x, new_y)
        
        # Update all edges
        for (u, v), line_id in self.edge_items.items():
            if u in self.node_positions and v in self.node_positions:
                u_x, u_y = self.node_positions[u]
                v_x, v_y = self.node_positions[v]
                self.canvas.coords(line_id, u_x, u_y, v_x, v_y)

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
        """Delete a node and all its incident edges from graph and UI."""
        if nid not in self.node_items:
            return

        try:
            # Delete from canvas
            circle, text = self.node_items[nid]
            self.canvas.delete(circle)
            self.canvas.delete(text)

            # Delete visual edges touching this node
            to_delete = [key for key in self.edge_items if nid in key]
            for key in to_delete:
                line = self.edge_items[key]
                self.canvas.delete(line)
                del self.edge_items[key]

            # Delete from backend graph
            self.graph.remove_node(nid)

            # Clean up tracking
            del self.node_positions[nid]
            del self.node_items[nid]
            if nid in self.node_categories:
                del self.node_categories[nid]

            if self.selected_node == nid:
                self.selected_node = None

            self.update_stats()
            self.show_notification(f"Person {nid} deleted", "success", 2000)
            logger.info(f"Node {nid} deleted successfully.")
        except Exception as e:
            logger.error(f"Error deleting node {nid}: {e}")
            self.show_notification(f"Error deleting node: {e}", "error", 3000)

    def delete_edge(self, u, v):
        """Delete an edge between u and v from graph and UI."""
        try:
            key = frozenset({u, v})

            # Remove from canvas
            if key in self.edge_items:
                self.canvas.delete(self.edge_items[key])
                del self.edge_items[key]

            # Remove from backend graph using the proper method
            self.graph.remove_edge(u, v)

            self.update_stats()
            self.show_notification(f"Connection {u}-{v} deleted", "success", 2000)
            logger.info(f"Edge {u}-{v} deleted successfully.")
        except Exception as e:
            logger.error(f"Error deleting edge {u}-{v}: {e}")
            self.show_notification(f"Error deleting edge: {e}", "error", 3000)
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
        """Export adjacency list representation of the graph."""
        if not self.graph.nodes:
            self.show_notification("Graph is empty", "warning", 2000)
            return

        try:
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
                self.show_notification("Adjacency list displayed", "success", 2000)
            elif choice == "save":
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    title="Save adjacency list"
                )
                if file_path:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    self.show_notification(f"Saved to {os.path.basename(file_path)}", "success", 2000)
                    logger.info(f"Adjacency list exported to {file_path}")
            else:
                self.show_notification("Action cancelled", "info", 1500)
        except Exception as e:
            logger.error(f"Error exporting adjacency list: {e}")
            self.show_notification(f"Error: {e}", "error", 3000)

    def export_adjacency_matrix(self):
        """Export adjacency matrix representation of the graph."""
        if not self.graph.nodes:
            self.show_notification("Graph is empty", "warning", 2000)
            return

        try:
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
                self.show_notification("Adjacency matrix displayed", "success", 2000)

            elif choice == "save":
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    title="Save adjacency matrix"
                )
                if file_path:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    self.show_notification(f"Saved to {os.path.basename(file_path)}", "success", 2000)
                    logger.info(f"Adjacency matrix exported to {file_path}")

            else:
                self.show_notification("Action cancelled", "info", 1500)
        except Exception as e:
            logger.error(f"Error exporting adjacency matrix: {e}")
            self.show_notification(f"Error: {e}", "error", 3000)
    def ask_export_action(self, title="Select Action", actions=None):
        """
        actions: list of tuples (button_text, return_value)
        Example:
        [
            ("Show", "show"),
            ("Save", "save"),
            ("Cancel", "cancel")
        ]
        """

        # Default actions (used by adjacency list & matrix)
        if actions is None:
            actions = [
                ("Show", "show"),
                ("Save", "save"),
                ("Cancel", "cancel"),
            ]

        popup = ctk.CTkToplevel(self.root)
        popup.title(title)
        popup.geometry("320x180")
        popup.grab_set()

        label = ctk.CTkLabel(
            popup,
            text="Choose an action:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(pady=10)

        selected = {"choice": None}

        btn_frame = ctk.CTkFrame(popup)
        btn_frame.pack(pady=10)

        # Create buttons dynamically
        for idx, (text, value) in enumerate(actions):
            def handler(val=value):
                selected["choice"] = val
                popup.destroy()

            ctk.CTkButton(
                btn_frame,
                text=text,
                width=100,
                command=handler
            ).grid(row=idx // 2, column=idx % 2, padx=5, pady=5)

        popup.wait_window()
        return selected["choice"]

    def measure_time(self, func, *args):
        """Measure execution time of a function."""
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        return result, (end - start)
    def run_performance_test(self):
        """Run performance tests for all algorithms."""
        if not self.graph.nodes:
            self.status_label.configure(text="Graph is empty.")
            return

        # Ask user what they want to do
        choice = self.ask_export_action(
            title="Performance Test",
            actions=[
                ("Show Report", "show"),
                ("Show Chart", "chart"),
                ("Save Report", "save"),
                ("Cancel", "cancel")
            ]
        )

        # If user canceled → stop
        if choice == "cancel" or choice is None:
            self.status_label.configure(text="Action cancelled.")
            return

        try:
            # Measure algorithm times
            results = {}

            start_node = min(self.graph.nodes.keys())
            end_node = max(self.graph.nodes.keys())

            # BFS
            _, results["BFS"] = self.measure_time(bfs, self.graph, start_node)

            # DFS
            _, results["DFS"] = self.measure_time(dfs, self.graph, start_node)

            # Dijkstra
            (_, _prev), results["Dijkstra"] = self.measure_time(dijkstra, self.graph, start_node)

            # A*
            (_, _prev, _), results["A*"] = self.measure_time(astar, self.graph, start_node, end_node)

            # Connected Components
            _, results["Connected Components"] = self.measure_time(connected_components, self.graph)

            # Graph Coloring
            _, results["Graph Coloring"] = self.measure_time(welsh_powell, self.graph)

            # Prepare text report
            report_lines = ["Performance Report (seconds):\n"]
            for key, value in results.items():
                report_lines.append(f"{key:<22} : {value:.6f}")
            report_text = "\n".join(report_lines)

            # Handle user action
            if choice == "show":
                self.show_text_popup("Performance Report", report_text)
                logger.info("Performance report displayed")

            elif choice == "save":
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt")],
                    title="Save Performance Report"
                )
                if file_path:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(report_text)
                    self.status_label.configure(text="Performance report saved.")
                    logger.info(f"Performance report saved to {file_path}")

            elif choice == "chart":
                self.show_performance_chart(results)
                logger.info("Performance chart displayed")

        except Exception as e:
            logger.error(f"Error running performance test: {e}")
            self.status_label.configure(text=f"Performance test error: {e}")
    def show_performance_chart(self, results):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Performance Chart")
        popup.geometry("960x820")
        popup.grab_set()

        labels = list(results.keys())
        values = list(results.values())

        # Create a dark-theme matplotlib figure
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)

        # Dark theme colors
        fig.patch.set_facecolor("#1a1a1a")
        ax.set_facecolor("#1e1e1e")

        # Bar colors
        bar_colors = ["#4A90E2", "#357ABD", "#2F6AA3", "#25527D", "#1D3F61", "#162D46"]

        bars = ax.bar(labels, values, color=bar_colors)

        # Title & labels styling
        ax.set_title("Algorithm Performance (Seconds)", color="white", fontsize=14, pad=12)
        ax.set_ylabel("Time (seconds)", color="white", fontsize=12)

        # Rotate x labels fully visible
        ax.tick_params(axis='x', colors='white', labelsize=8, rotation=25)
        ax.tick_params(axis='y', colors='white', labelsize=8)

        # Add value labels above bars
        for bar, val in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{val:.6f}",
                ha='center',
                va='bottom',
                color='white',
                fontsize=9,
                fontweight='bold',
                rotation=0
            )

        # Remove top/right borders
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")

        # Render chart inside popup window
        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)

    def export_algorithm_results(self):
        """Export results from last executed algorithm."""
        if not self.last_algorithm_result:
            self.show_notification("No algorithm results to export", "warning", 2000)
            return
        
        try:
            content = f"Algorithm: {self.last_algorithm_name}\n"
            content += f"Graph Nodes: {len(self.graph.nodes)}\n"
            content += f"Graph Edges: {len(self.graph.edges)}\n"
            content += "=" * 50 + "\n"
            content += str(self.last_algorithm_result)
            
            choice = self.ask_export_action("Export Results")
            
            if choice == "show":
                self.show_text_popup(f"{self.last_algorithm_name} Results", content)
                self.show_notification("Results displayed", "success", 2000)
            elif choice == "save":
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    title=f"Save {self.last_algorithm_name} results"
                )
                if file_path:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    self.show_notification(f"Saved to {os.path.basename(file_path)}", "success", 2000)
                    logger.info(f"Algorithm results exported to {file_path}")
        except Exception as e:
            logger.error(f"Error exporting results: {e}")
            self.show_notification(f"Export failed: {str(e)[:50]}", "error", 3000)

    # =================================================================
    # Sidebar
    # =================================================================
    def build_sidebar(self):
        """Build organized sidebar with collapsible sections."""
        # Scrollable frame for sidebar
        scrollable = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        scrollable.pack(fill="both", expand=True)

        # Start node entry
        ctk.CTkLabel(scrollable, text="Start Node", font=ctk.CTkFont(size=13, weight="bold")).pack(pady=(10, 0), padx=10, anchor="w")
        self.start_entry = ctk.CTkEntry(scrollable, placeholder_text="Default: 1", font=ctk.CTkFont(size=12))
        self.start_entry.pack(pady=(4, 12), padx=10, fill="x", ipady=6)

        btn_cfg = {"height": 42, "corner_radius": 6, "font": ctk.CTkFont(size=12, weight="bold")}

        # Section 1: Traversal Algorithms
        self.create_section(scrollable, "📊 Traversal", [
            ("BFS", self.run_bfs),
            ("DFS", self.run_dfs),
        ], btn_cfg)

        # Section 2: Shortest Path
        self.create_section(scrollable, "🛤️ Shortest Path", [
            ("Dijkstra", self.run_dijkstra),
            ("A* Search", self.run_astar),
        ], btn_cfg)

        # Section 3: Analysis
        self.create_section(scrollable, "🔍 Analysis", [
            ("Components", self.run_components),
            ("Centrality", self.run_centrality),
            ("Coloring", self.run_coloring),
        ], btn_cfg)

        # Section 4: Data Export
        self.create_section(scrollable, "💾 Export", [
            ("Adjacency List", self.export_adjacency_list),
            ("Adjacency Matrix", self.export_adjacency_matrix),
            ("Algorithm Results", self.export_algorithm_results),
        ], btn_cfg)

        # Section 5: Data Management
        self.create_section(scrollable, "📁 Data", [
            ("Load CSV", self.show_sample_dialog),
            ("Save JSON", self.save_graph_to_json),
            ("Load JSON", self.load_graph_from_json),
        ], btn_cfg)

        # Section 6: Analysis Tools
        self.create_section(scrollable, "⚡ Tools", [
            ("Performance", self.run_performance_test),
        ], btn_cfg)

        # Clear button (at bottom)
        ctk.CTkButton(
            scrollable,
            text="🗑️ Clear Graph",
            command=self.clear_graph,
            height=36,
            fg_color="#a83232",
            hover_color="#7a2020",
            font=ctk.CTkFont(size=11)
        ).pack(pady=(20, 10), padx=10, fill="x")

    def create_section(self, parent, title: str, buttons: List[Tuple[str, callable]], btn_config: dict):
        """Create a collapsible section with buttons."""
        section_frame = ctk.CTkFrame(parent, fg_color="#1a1a22", corner_radius=8)
        section_frame.pack(pady=8, padx=10, fill="x")

        # Section header
        header = ctk.CTkFrame(section_frame, fg_color="transparent", height=42)
        header.pack(fill="x", padx=10, pady=10)
        header.pack_propagate(False)

        ctk.CTkLabel(header, text=title, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")

        # Buttons
        for btn_text, cmd in buttons:
            btn = ctk.CTkButton(section_frame, text=btn_text, command=cmd, **btn_config)
            btn.pack(pady=4, padx=10, fill="x")



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
            self.show_notification(f"Selected node {clicked_id} · Click another to connect", "info", 3000)
        else:
            if clicked_id != self.selected_node:
                self.create_edge(self.selected_node, clicked_id)
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
        popup.geometry("320x360")
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

        # Category selector
        ctk.CTkLabel(popup, text="Category:", font=ctk.CTkFont(size=11, weight="bold")).pack(pady=(8, 4), padx=20, anchor="w")
        category_var = tk.StringVar(value="default")
        category_menu = ctk.CTkOptionMenu(
            popup,
            values=list(self.category_colors.keys()),
            variable=category_var
        )
        category_menu.pack(pady=4, padx=20, fill="x")

        error_label = ctk.CTkLabel(popup, text="", text_color="red")
        error_label.pack(pady=2)

        def on_confirm():
            try:
                name = name_entry.get().strip() or f"User {self.next_node_id}"
                activity = float(act_entry.get() or 0.5)
                interaction = float(inter_entry.get() or 0.0)
                conn_count = float(conn_entry.get() or 0.0)
                category = category_var.get()
            except ValueError:
                error_label.configure(text="Enter numeric values for activity/interaction/connections.")
                return

            popup.destroy()
            self.create_node(x, y, name, activity, interaction, conn_count, category)

        btn_frame = ctk.CTkFrame(popup)
        btn_frame.pack(pady=10, fill="x")

        ctk.CTkButton(btn_frame, text="Cancel", command=popup.destroy).pack(side="left", padx=10, expand=True)
        ctk.CTkButton(btn_frame, text="Create", command=on_confirm).pack(side="right", padx=10, expand=True)
    def open_node_info_popup(self, nid: int):
            """Show editable information popup for a node."""

            if nid not in self.graph.nodes:
                return

            node = self.graph.nodes[nid]
            neighbors = sorted(self.graph.get_neighbors(nid))
            degree = len(neighbors)

            popup = ctk.CTkToplevel(self.root)
            popup.title(f"Person {nid} info")
            popup.geometry("360x430")
            popup.grab_set()

            # -------------------------------------------------
            # Title
            # -------------------------------------------------
            ctk.CTkLabel(
                popup,
                text=f"Person ID: {nid}",
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(pady=(10, 5))

            # -------------------------------------------------
            # Editable fields
            # -------------------------------------------------

            # Name
            ctk.CTkLabel(popup, text="Name:").pack(anchor="w", padx=20)
            name_entry = ctk.CTkEntry(popup)
            name_entry.insert(0, node.name or f"User {nid}")
            name_entry.pack(pady=(0, 8), padx=20, fill="x")

            # Activity
            ctk.CTkLabel(popup, text="Activity (0-1):").pack(anchor="w", padx=20)
            act_entry = ctk.CTkEntry(popup)
            act_entry.insert(0, str(node.activity))
            act_entry.pack(pady=(0, 8), padx=20, fill="x")

            # Interaction
            ctk.CTkLabel(popup, text="Interaction:").pack(anchor="w", padx=20)
            inter_entry = ctk.CTkEntry(popup)
            inter_entry.insert(0, str(node.interaction))
            inter_entry.pack(pady=(0, 8), padx=20, fill="x")

            # Connection count
            ctk.CTkLabel(popup, text="Connection Count:").pack(anchor="w", padx=20)
            conn_entry = ctk.CTkEntry(popup)
            conn_entry.insert(0, str(node.connection_count))
            conn_entry.pack(pady=(0, 8), padx=20, fill="x")

            # -------------------------------------------------
            # Degree + Neighbors (read only)
            # -------------------------------------------------
            info_label = ctk.CTkLabel(
                popup,
                text=f"Degree: {degree}   Neighbors: {', '.join(map(str, neighbors)) or 'None'}",
                wraplength=300,
                justify="left"
            )
            info_label.pack(pady=(8, 4))

            error_label = ctk.CTkLabel(popup, text="", text_color="red")
            error_label.pack(pady=(2, 4))

            # -------------------------------------------------
            # Save Button (Update)
            # -------------------------------------------------
            def on_save():
                """Update node + recompute weights for connected edges."""

                try:
                    new_name = name_entry.get().strip() or f"User {nid}"
                    new_activity = float(act_entry.get())
                    new_interaction = float(inter_entry.get())
                    new_conn = float(conn_entry.get())

                except ValueError:
                    error_label.configure(text="Please enter valid numeric values.")
                    return

                # Update node object
                self.graph.update_node(
                    nid,
                    name=new_name,
                    activity=new_activity,
                    interaction=new_interaction,
                    connection_count=new_conn,
                )

                # Recompute weights for edges connected to the node
                for nbr in list(self.graph.get_neighbors(nid)):
                    if self.graph.has_edge(nid, nbr):
                        self.recompute_edge_weight(nid, nbr)

                popup.destroy()
                self.status_label.configure(text=f"Person {nid} updated successfully.")
                self.reset_visual_style()

            # -------------------------------------------------
            # Delete Button
            # -------------------------------------------------
            def on_delete():
                popup.destroy()
                self.delete_node(nid)

            btn_frame = ctk.CTkFrame(popup)
            btn_frame.pack(pady=15, fill="x")

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
                text="Save Changes",
                command=on_save
            )
            save_btn.pack(side="right", padx=10, expand=True)


    # =================================================================
    # Create node + draw on canvas
    # =================================================================
    def create_node(self, x, y, name, activity, interaction, connection_count, category="default"):
        nid = self.next_node_id
        self.next_node_id += 1

        self.graph.add_node(
            nid,
            name=name,
            activity=activity,
            interaction=interaction,
            connection_count=connection_count
        )

        # Get color based on category
        color = self.category_colors.get(category, self.category_colors["default"])
        self.node_categories[nid] = category

        circle = self.canvas.create_oval(
            x - self.node_radius, y - self.node_radius,
            x + self.node_radius, y + self.node_radius,
            fill=color,
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
        
        # Initialize original positions for zoom
        if not hasattr(self, 'original_positions'):
            self.original_positions = {}
        self.original_positions[nid] = (x, y)

        self.update_stats()
        self.show_notification(f"Person {nid} created ({category})", "success", 2000)


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
    
    def apply_gradient_coloring(self, node_values: Dict[int, float]):
        """Apply gradient coloring to nodes based on their values."""
        if not node_values:
            return
        
        min_val = min(node_values.values())
        max_val = max(node_values.values())
        
        # Generate colors for each node
        self.gradient_map = {}
        for nid, value in node_values.items():
            color = self.generate_gradient_color(value, min_val, max_val)
            self.gradient_map[nid] = color
            self.highlight_node_fill(nid, color)
    
    def clear_gradient_coloring(self):
        """Clear gradient coloring and restore original colors."""
        for nid in self.gradient_map:
            if nid in self.node_categories:
                category = self.node_categories[nid]
                color = self.category_colors.get(category, self.category_colors["default"])
                self.highlight_node_fill(nid, color)
        self.gradient_map.clear()


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

        weight = self._calculate_edge_weight(n1, n2)
        self.graph.add_edge(u, v, weight)
        
        self.update_stats()
        self.show_notification(f"Connected {u} ↔ {v}", "success", 2000)

    def _calculate_edge_weight(self, node1, node2):
        """Calculate edge weight based on node attributes."""
        return 1.0 / (
            1.0 + math.sqrt(
                (node1.activity - node2.activity)**2 +
                (node1.interaction - node2.interaction)**2 +
                (node1.connection_count - node2.connection_count)**2
            )
        )
    
    def generate_gradient_color(self, value, min_val=0, max_val=1):
        """Generate a gradient color from blue (low) to red (high)."""
        # Normalize value
        if max_val == min_val:
            norm = 0.5
        else:
            norm = (value - min_val) / (max_val - min_val)
        norm = max(0, min(1, norm))  # Clamp to 0-1
        
        # Create gradient: Blue -> Cyan -> Green -> Yellow -> Red
        if norm < 0.25:
            # Blue to Cyan
            t = norm / 0.25
            r = int(0 + (0 - 0) * t)
            g = int(0 + (255 - 0) * t)
            b = int(255 + (255 - 255) * t)
        elif norm < 0.5:
            # Cyan to Green
            t = (norm - 0.25) / 0.25
            r = int(0 + (0 - 0) * t)
            g = int(255)
            b = int(255 + (0 - 255) * t)
        elif norm < 0.75:
            # Green to Yellow
            t = (norm - 0.5) / 0.25
            r = int(0 + (255 - 0) * t)
            g = int(255)
            b = int(0)
        else:
            # Yellow to Red
            t = (norm - 0.75) / 0.25
            r = int(255)
            g = int(255 + (0 - 255) * t)
            b = int(0)
        
        return f"#{r:02x}{g:02x}{b:02x}"

    def recompute_edge_weight(self, u, v):
        """Recompute and update edge weight when node attributes change."""
        if self.graph.has_edge(u, v):
            n1 = self.graph.nodes[u]
            n2 = self.graph.nodes[v]
            new_weight = self._calculate_edge_weight(n1, n2)
            self.graph.update_edge_weight(u, v, new_weight)


    # =================================================================
    # Graph reset / load
    # =================================================================
    def clear_graph(self):
        """Clear all nodes and edges from the graph."""
        if not self.graph.nodes:
            self.show_notification("Graph is already empty", "info", 2000)
            return

        # Confirm deletion
        if messagebox.askyesno("Clear Graph", "Are you sure you want to clear the entire graph?"):
            try:
                self.canvas.delete("all")
                self.graph.clear()

                self.node_positions.clear()
                self.node_items.clear()
                self.edge_items.clear()
                self.node_categories.clear()
                if hasattr(self, 'original_positions'):
                    self.original_positions.clear()

                self.next_node_id = 1
                self.selected_node = None
                self.canvas_scale = 1.0

                self.update_stats()
                self.show_notification("Graph cleared", "success", 2000)
                logger.info("Graph cleared successfully")
            except Exception as e:
                logger.error(f"Error clearing graph: {e}")
                self.show_notification(f"Error: {str(e)[:50]}", "error", 3000)
        else:
            self.show_notification("Clear cancelled", "info", 1500)
    def save_graph_to_json(self):
        """Save the current graph to a JSON file."""
        if not self.graph.nodes:
            self.show_notification("Graph is empty", "warning", 2000)
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Save graph as JSON"
        )
        if not file_path:
            return

        try:
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

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.show_notification(f"Saved to {os.path.basename(file_path)}", "success", 2000)
            logger.info(f"Graph saved to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save JSON: {e}")
            self.show_notification(f"Save failed: {str(e)[:50]}", "error", 3000)
    def load_graph_from_json(self):
        """Load graph from a JSON file."""
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
            logger.error(f"Failed to read JSON: {e}")
            self.show_notification(f"Failed to read JSON: {str(e)[:50]}", "error", 3000)
            return

        try:
            # Reset current graph and visuals
            self.canvas.delete("all")
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
                interaction = float(node_data.get("interaction", 0.0))
                connection_count = float(node_data.get("connection_count", 0.0))

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

            self.update_stats()
            self.show_notification(f"Loaded {os.path.basename(file_path)}", "success", 2000)
            logger.info(f"Graph loaded successfully from {file_path}")
        except Exception as e:
            logger.error(f"Error loading graph: {e}")
            self.show_notification(f"Load failed: {str(e)[:50]}", "error", 3000)
            self.graph = Graph()  # Reset to empty graph on error


    
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
                          done_text="Traversal done.", use_gradient=False):

        if not order:
            return

        self.reset_visual_style()
        
        # If using gradient, map nodes to colors based on traversal order
        if use_gradient:
            gradient_values = {nid: i / len(order) for i, nid in enumerate(order)}
            self.apply_gradient_coloring(gradient_values)

        def step(i):
            if i >= len(order):
                self.status_label.configure(text=done_text)
                return

            nid = order[i]
            
            # Use gradient color if enabled, otherwise use solid color
            if use_gradient:
                color = self.gradient_map.get(nid, node_color)
            else:
                color = node_color
            
            self.highlight_node_fill(nid, color)
            
            # Add glowing outline for current node
            if nid in self.node_items:
                circle, _ = self.node_items[nid]
                self.canvas.itemconfig(circle, outline="#fbbf24", width=3)

            if i > 0:
                u = order[i-1]
                v = order[i]
                self.highlight_edge(u, v, edge_color, width=3)
                # Remove highlight from previous node
                if u in self.node_items:
                    circle, _ = self.node_items[u]
                    self.canvas.itemconfig(circle, outline="#ffffff", width=1)

            self.root.after(delay_ms, lambda: step(i+1))

        step(0)
    def show_sample_dialog(self):
        """Show dialog to select which sample CSV to load."""
        choice = self.ask_export_action(
            title="Load Sample",
            actions=[
                ("Load Small Sample", "small"),
                ("Load Medium Sample", "medium"),
                ("Cancel", "cancel")
            ]
        )

        if choice == "small":
            self.load_sample_graph("sample_small.csv")
        elif choice == "medium":
            self.load_sample_graph("sample_medium.csv")
        else:
            self.status_label.configure(text="Action cancelled.")

    def load_sample_graph(self, filename="sample_small.csv"):
        """Load sample CSV graph and display it in a circular layout."""
        try:
            logger.info(f"Loading sample graph: {filename}")

            # Determine the project root
            ui_dir = os.path.dirname(os.path.abspath(__file__))
            src_dir = os.path.dirname(ui_dir)
            project_root = os.path.dirname(src_dir)

            csv_path = os.path.join(project_root, "data", filename)

            if not os.path.exists(csv_path):
                logger.error(f"CSV not found: {csv_path}")
                self.show_notification(f"CSV not found", "error", 3000)
                return

            # Reset UI
            self.canvas.delete("all")
            self.node_positions.clear()
            self.node_items.clear()
            self.edge_items.clear()
            self.node_categories.clear()
            if hasattr(self, 'original_positions'):
                self.original_positions.clear()
            self.selected_node = None
            self.canvas_scale = 1.0

            # Load Backend Graph using enhanced loader
            self.graph = GraphLoader.load_from_csv(csv_path)

            # Layout nodes in a circle
            width = self.canvas.winfo_width() or 900
            height = self.canvas.winfo_height() or 700
            cx, cy = width // 2, height // 2
            radius = min(width, height) // 2 - 120

            node_ids = sorted(self.graph.nodes.keys())
            n = len(node_ids) if node_ids else 1

            # Initialize original positions
            self.original_positions = {}

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
                self.original_positions[nid] = (x, y)
                self.node_items[nid] = (circle, text)

            # Draw edges
            for edge in self.graph.get_edges():
                u, v = edge.u, edge.v
                x1, y1 = self.node_positions[u]
                x2, y2 = self.node_positions[v]
                line_id = self.canvas.create_line(
                    x1, y1, x2, y2, fill="#9CA3AF", width=2
                )
                self.edge_items[frozenset({u, v})] = line_id

            # Update next node ID
            if self.graph.nodes:
                self.next_node_id = max(self.graph.nodes.keys()) + 1
            else:
                self.next_node_id = 1

            self.update_stats()
            self.show_notification(f"Loaded {len(self.graph.nodes)} nodes · {len(self.graph.edges)} edges", "success", 2000)
            logger.info(f"Sample graph loaded: {len(self.graph.nodes)} nodes, {len(self.graph.edges)} edges.")
        except Exception as e:
            logger.error(f"Error loading sample graph: {e}")
            self.show_notification(f"Load failed: {str(e)[:50]}", "error", 3000)
            self.graph = Graph()  # Reset to empty graph on error


    # =================================================================
    # Algorithm actions
    # =================================================================
    def run_bfs(self):
        """Run BFS algorithm and animate the traversal."""
        if not self.graph.nodes:
            self.show_notification("Graph is empty", "warning", 2000)
            return

        start = self.get_start_node()
        if start not in self.graph.nodes:
            self.show_notification(f"Start node {start} not found", "error", 2000)
            return

        try:
            order = bfs(self.graph, start)
            self.show_notification(f"BFS from {start} · {len(order)} nodes", "info", 2000)
            
            # Apply gradient coloring based on traversal order
            gradient_values = {nid: order.index(nid) / len(order) for nid in order}
            self.apply_gradient_coloring(gradient_values)
            
            self.animate_traversal(order, node_color="#f97316", edge_color="#f97316", 
                                 done_text="BFS completed", use_gradient=False)
            logger.info(f"BFS completed from node {start}")
        except Exception as e:
            logger.error(f"BFS error: {e}")
            self.show_notification(f"BFS error: {str(e)[:50]}", "error", 3000)


    def run_dfs(self):
        """Run DFS algorithm and animate the traversal."""
        if not self.graph.nodes:
            self.show_notification("Graph is empty", "warning", 2000)
            return

        start = self.get_start_node()
        if start not in self.graph.nodes:
            self.show_notification(f"Start node {start} not found", "error", 2000)
            return

        try:
            order = dfs(self.graph, start)
            self.show_notification(f"DFS from {start} · {len(order)} nodes", "info", 2000)
            
            # Apply gradient coloring based on traversal order
            gradient_values = {nid: order.index(nid) / len(order) for nid in order}
            self.apply_gradient_coloring(gradient_values)
            
            self.animate_traversal(order, node_color="#3b82f6", edge_color="#3b82f6", 
                                 done_text="DFS completed", use_gradient=False)
            logger.info(f"DFS completed from node {start}")
        except Exception as e:
            logger.error(f"DFS error: {e}")
            self.show_notification(f"DFS error: {str(e)[:50]}", "error", 3000)


    def run_dijkstra(self):
        """Run Dijkstra algorithm and show the shortest path."""
        if not self.graph.nodes:
            self.show_notification("Graph is empty", "warning", 2000)
            return

        start = self.get_start_node()
        if start not in self.graph.nodes:
            self.show_notification(f"Start node {start} not found", "error", 2000)
            return

        try:
            target = max(self.graph.nodes.keys())
            dist, prev = dijkstra(self.graph, start)
            path = reconstruct_path(prev, start, target)

            if not path:
                self.show_notification(f"No path {start}→{target}", "warning", 2000)
                logger.warning(f"No path found from {start} to {target}")
                return

            self.reset_visual_style()
            distance = dist.get(target, float('inf'))
            self.show_notification(f"Dijkstra {start}→{target}: {distance:.4f}", "success", 2000)
            
            # Apply gradient coloring based on distance from start
            gradient_values = {nid: min(dist[nid] / (distance if distance > 0 else 1), 1.0) for nid in self.graph.nodes}
            self.apply_gradient_coloring(gradient_values)
            
            self.animate_traversal(path, node_color="#22c55e", edge_color="#22c55e", 
                                 done_text="Dijkstra completed", use_gradient=False)
            logger.info(f"Dijkstra completed: {start} -> {target}")
        except Exception as e:
            logger.error(f"Dijkstra error: {e}")
            self.show_notification(f"Dijkstra error: {str(e)[:50]}", "error", 3000)


    def run_astar(self):
        """Run A* algorithm and show the path."""
        if not self.graph.nodes:
            self.show_notification("Graph is empty", "warning", 2000)
            return

        start = self.get_start_node()
        if start not in self.graph.nodes:
            self.show_notification(f"Start node {start} not found", "error", 2000)
            return

        try:
            target = max(self.graph.nodes.keys())
            dist, prev, path = astar(self.graph, start, target)
            
            if not path:
                self.show_notification(f"No A* path {start}→{target}", "warning", 2000)
                logger.warning(f"No A* path found from {start} to {target}")
                return

            self.reset_visual_style()
            distance = dist.get(target, float('inf'))
            self.show_notification(f"A* {start}→{target}: {distance:.4f}", "success", 2000)
            
            # Apply gradient coloring based on distance
            gradient_values = {nid: min(dist[nid] / (distance if distance > 0 else 1), 1.0) for nid in self.graph.nodes}
            self.apply_gradient_coloring(gradient_values)
            
            self.animate_traversal(path, node_color="#eab308", edge_color="#eab308", 
                                 done_text="A* completed", use_gradient=False)
            logger.info(f"A* completed: {start} -> {target}")
        except Exception as e:
            logger.error(f"A* error: {e}")
            self.show_notification(f"A* error: {str(e)[:50]}", "error", 3000)


    def run_components(self):
        """Find and visualize connected components."""
        if not self.graph.nodes:
            self.show_notification("Graph is empty", "warning", 2000)
            return

        try:
            comps = connected_components(self.graph)
            self.reset_visual_style()

            palette = ["#22c55e", "#3b82f6", "#a855f7", "#ec4899", "#eab308", "#14b8a6", "#f97316"]

            for i, comp in enumerate(comps):
                color = palette[i % len(palette)]
                for nid in comp:
                    self.highlight_node_fill(nid, color)
                    # Add outline to enhance component visibility
                    if nid in self.node_items:
                        circle, _ = self.node_items[nid]
                        next_color = palette[(i + 1) % len(palette)]
                        self.canvas.itemconfig(circle, outline=next_color, width=2)

            msg = f"{len(comps)} component(s) found"
            self.show_notification(msg, "success", 2000)
            logger.info(f"Connected components: {len(comps)}")
        except Exception as e:
            logger.error(f"Components error: {e}")
            self.show_notification(f"Components error: {str(e)[:50]}", "error", 3000)


    def run_centrality(self):
        """Find and highlight the most central nodes."""
        if not self.graph.nodes:
            self.show_notification("Graph is empty", "warning", 2000)
            return

        try:
            results = degree_centrality(self.graph, min(5, len(self.graph.nodes)))
            important = [nid for nid, deg in results]

            self.reset_visual_style()
            
            # Apply gradient coloring to all nodes based on degree
            all_degrees = {nid: len(self.graph.get_neighbors(nid)) for nid in self.graph.nodes}
            max_degree = max(all_degrees.values()) if all_degrees else 1
            normalized_degrees = {nid: deg / max_degree for nid, deg in all_degrees.items()}
            self.apply_gradient_coloring(normalized_degrees)

            # Highlight top central nodes with extra border
            for nid in important:
                if nid in self.node_items:
                    circle, _ = self.node_items[nid]
                    self.canvas.itemconfig(circle, outline="#fbbf24", width=3)

            txt = ", ".join(f"{nid}({deg})" for nid, deg in results)
            self.show_notification(f"Central nodes: {txt}", "success", 2000)
            logger.info(f"Centrality analysis: {txt}")
        except Exception as e:
            logger.error(f"Centrality error: {e}")
            self.show_notification(f"Centrality error: {str(e)[:50]}", "error", 3000)


    def run_coloring(self):
        """Color the graph with minimum number of colors."""
        if not self.graph.nodes:
            self.show_notification("Graph is empty", "warning", 2000)
            return

        try:
            coloring = welsh_powell(self.graph)
            palette = ["#22c55e", "#3b82f6", "#a855f7", "#ec4899", "#eab308", "#14b8a6", "#f97316", "#06b6d4"]

            self.reset_visual_style()
            
            # Enhanced visual feedback with gradient
            max_color = max(coloring.values()) if coloring else 0
            gradient_values = {nid: color_idx / (max_color if max_color > 0 else 1) 
                             for nid, color_idx in coloring.items()}

            for nid, color_idx in coloring.items():
                color = palette[color_idx % len(palette)]
                self.highlight_node_fill(nid, color)
                # Add subtle glow based on color group
                if nid in self.node_items:
                    circle, _ = self.node_items[nid]
                    self.canvas.itemconfig(circle, outline=palette[(color_idx + 1) % len(palette)], width=2)

            msg = f"Graph colored with {max_color + 1} colors"
            self.show_notification(msg, "success", 2000)
            logger.info(f"Graph coloring completed: {max_color + 1} colors used")
        except Exception as e:
            logger.error(f"Coloring error: {e}")
            self.show_notification(f"Coloring error: {str(e)[:50]}", "error", 3000)



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
