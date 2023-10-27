from tkinter import ttk
from tkinter import *


class GridFrame:
    def __init__(self, parent):
        self.parent = parent
        self.place_dir = 'one_widget'
        self.f = ttk.Frame(parent)
        self._place_idx = 0
        self._widget_sizes = []
        self._children_frames = []
        self._children = []

    def place(self, widget):
        if self.place_dir == 'one_widget':
            widget.grid(row=0, column=0, sticky=(N, S, E, W))
            self._children = [widget]
        elif self.place_dir == "vertical":
            widget.grid(row=self._place_idx, column=0, sticky=(N, S, E, W))
            self._children.append(widget)
            self._place_idx += 1
        elif self.place_dir == "horizontal":
            widget.grid(row=0, column=self._place_idx, sticky=(N, S, E, W))
            self._children.append(widget)
            self._place_idx += 1
        else:
            raise Exception("frame grid direction is invalid")

    def set_config(self):
        if self.place_dir == 'one_widget':
            self.f.columnconfigure(0, weight=1)
            self.f.rowconfigure(0, weight=1)
        elif self.place_dir == "vertical":
            self.f.columnconfigure(0, weight=1)
            for i, size in enumerate(self._widget_sizes):
                self.f.grid_rowconfigure(i, weight=size)
        elif self.place_dir == "horizontal":
            for i, size in enumerate(self._widget_sizes):
                self.f.grid_columnconfigure(i, weight=size)
            self.f.rowconfigure(0, weight=1)
        else:
            raise Exception("frame grid direction is invalid")
        for child_frame in self._children_frames:
            child_frame.set_config()

    def set_horizontal_place_widget(self, sizes: list):
        assert self.place_dir == 'one_widget', "this frame is already parted"
        self.place_dir = 'horizontal'
        self._widget_sizes = sizes

    def set_vertical_place_widget(self, sizes: list):
        assert self.place_dir == 'one_widget', "this frame is already parted"
        self.place_dir = 'vertical'
        self._widget_sizes = sizes

    def add_horizontal_place_child_frame(self, sizes: list) -> 'GridFrame':
        grid_frame = GridFrame(self.f)
        grid_frame.set_horizontal_place_widget(sizes)
        self._children_frames.append(grid_frame)
        self.place(grid_frame.f)
        return grid_frame

    def add_vertical_place_child_frame(self, sizes: list) -> 'GridFrame':
        grid_frame = GridFrame(self.f)
        grid_frame.set_vertical_place_widget(sizes)
        self._children_frames.append(grid_frame)
        self.place(grid_frame.f)
        return grid_frame

    def add_text_box(self) -> Text:
        t = Text(self.f, fg="white", bg="black", wrap=WORD, width=0, height=0)
        self.place(t)
        t.insert(END, "not initialized")
        return t

    def add_canvas(self) -> Canvas:
        c = Canvas(self.f, bg="white", width=0, height=0)
        self.place(c)
        return c

    def add_listbox(self) -> Listbox:
        lb = Listbox(self.f, bg="white", width=0, height=0)
        self.place(lb)
        return lb
