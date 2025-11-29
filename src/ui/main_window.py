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
            on_load_sample=self.load_sample_graph
        )
        self.controls.pack(fill=tk.Y, expand=False)

    def load_sample_graph(self):
        """
        Load the sample_small.csv file from the data folder and draw the graph.
        """

        # Move 3 levels up: ui → src → project root
        project_root = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )

        csv_path = os.path.join(project_root, "data", "sample_small.csv")

        print("CSV path:", csv_path)  # Debug print

        # Load and draw
        self.graph = GraphLoader.load_from_csv(csv_path)
        self.canvas.set_graph(self.graph)
        self.canvas.draw_graph()


