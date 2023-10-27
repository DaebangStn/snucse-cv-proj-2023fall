from gui.text_window import TextWindow
from gui.grid_frame import GridFrame


class LogFrame:
    def __init__(self, parent: GridFrame):
        self._gf = parent.add_horizontal_place_child_frame([1])
        self._log_window = self._gf.add_log_window()
        self._scrollbar = self._gf.add_scrollbar()
        self._log_window.set_scrollbar(self._scrollbar)
