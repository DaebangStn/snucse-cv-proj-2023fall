from tkinter import *
from tkinter import ttk
from gui.text_window import TextWindow, LogWindow, CommandWindow
from gui.photo_manager import PhotoManager
from gui.workstation_frame import WorkstationFrame


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

    def add_ws_frame(self) -> WorkstationFrame:
        ws = WorkstationFrame(self)
        self.place(ws.f)
        self._children.append(ws)
        return ws

    def add_text_window(self) -> TextWindow:
        t = TextWindow(self)
        self.place(t)
        return t

    def add_log_window(self) -> LogWindow:
        t = LogWindow(self)
        self.place(t)
        t.append("logger not initialized")
        return t

    def add_command_window(self) -> CommandWindow:
        t = CommandWindow(self)
        self.place(t)
        return t

    def add_photo_manager(self) -> PhotoManager:
        p = PhotoManager(self)
        self.place(p)
        return p

    def add_canvas(self) -> Canvas:
        c = Canvas(self.f, bg="white", width=0, height=0)
        self.place(c)
        return c

    def add_listbox(self) -> Listbox:
        lb = Listbox(self.f, bg="white", width=0, height=0)
        self.place(lb)
        return lb

    def add_scrollbar(self) -> Scrollbar:
        sb = Scrollbar(self.f, orient=VERTICAL, width=15)
        self.place(sb)
        return sb

    def get_children(self):
        return self._children

    def get_children_frames(self):
        return self._children_frames
