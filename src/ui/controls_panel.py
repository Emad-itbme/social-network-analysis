import tkinter as tk


class ControlsPanel(tk.Frame):
    """
    Side panel containing controls to run algorithms and load graphs.
    """

    def __init__(self, master, callbacks={}, **kwargs):
        super().__init__(master, **kwargs)

        self.callbacks = callbacks

        # Load sample graph
        btn_load = tk.Button(self, text="Load Sample Graph",
                             command=self.callbacks.get("load_sample"))
        btn_load.pack(pady=8, fill=tk.X)

        # BFS
        btn_bfs = tk.Button(self, text="Run BFS",
                            command=self.callbacks.get("run_bfs"))
        btn_bfs.pack(pady=8, fill=tk.X)

        # DFS
        btn_dfs = tk.Button(self, text="Run DFS",
                            command=self.callbacks.get("run_dfs"))
        btn_dfs.pack(pady=8, fill=tk.X)

        # Dijkstra
        btn_dijkstra = tk.Button(self, text="Run Dijkstra",
                                 command=self.callbacks.get("run_dijkstra"))
        btn_dijkstra.pack(pady=8, fill=tk.X)

        # A*
        btn_astar = tk.Button(self, text="Run A*",
                              command=self.callbacks.get("run_astar"))
        btn_astar.pack(pady=8, fill=tk.X)

        # Connected components
        btn_cc = tk.Button(self, text="Connected Components",
                           command=self.callbacks.get("run_components"))
        btn_cc.pack(pady=8, fill=tk.X)

        # Degree Centrality
        btn_dc = tk.Button(self, text="Degree Centrality",
                           command=self.callbacks.get("run_centrality"))
        btn_dc.pack(pady=8, fill=tk.X)

        # Welsh–Powell Coloring
        btn_wp = tk.Button(self, text="Graph Coloring",
                           command=self.callbacks.get("run_coloring"))
        btn_wp.pack(pady=8, fill=tk.X)

        # Quit
        btn_quit = tk.Button(self, text="Quit", command=self._handle_quit)
        btn_quit.pack(pady=8, fill=tk.X)

    def _handle_quit(self):
        self.winfo_toplevel().quit()
