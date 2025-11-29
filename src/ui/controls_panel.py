import tkinter as tk


class ControlsPanel(tk.Frame):
    """
    Side panel containing basic controls (buttons).
    """

    def __init__(self, master, on_load_sample=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_load_sample = on_load_sample

        load_btn = tk.Button(self, text="Load Sample Graph",
                             command=self._handle_load_sample)
        load_btn.pack(pady=10, fill=tk.X)

        quit_btn = tk.Button(self, text="Quit",
                             command=self._handle_quit)
        quit_btn.pack(pady=10, fill=tk.X)

    def _handle_load_sample(self):
        if self.on_load_sample is not None:
            self.on_load_sample()

    def _handle_quit(self):
        self.winfo_toplevel().quit()
