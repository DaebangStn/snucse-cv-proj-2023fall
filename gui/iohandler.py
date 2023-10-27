from gui.grid_frame import GridFrame
from gui.text_window import CommandWindow, LogWindow


class IOHandler:
    def __init__(self, root: GridFrame):
        self._root = root
        self._attach_grid_frame(root)
        self._clear_log()
        self._log("IOHandler initialized")

    def _attach_grid_frame(self, gf: GridFrame):
        for child in gf.get_children():
            print("attaching : ", child.__class__.__name__)
            if isinstance(child, GridFrame):
                pass
            elif isinstance(child, LogWindow):
                self._attach_log_window(child)
            elif isinstance(child, CommandWindow):
                self._attach_command_window(child)
        for frame in gf.get_children_frames():
            self._attach_grid_frame(frame)

    def _attach_log_window(self, log_window: LogWindow):
        assert not hasattr(self, '_log_window'), "log window already attached"
        self._log_window = log_window

    def _attach_command_window(self, command_window: CommandWindow):
        assert not hasattr(self, '_command_window'), "command window already attached"
        self._command_window = command_window
        self._command_window.bind_handler('<Return>', self._run_command)

    def _log(self, text: str):
        assert hasattr(self, '_log_window'), "log window not attached"
        self._log_window.log(text)

    def _clear_log(self):
        assert hasattr(self, '_log_window'), "log window not attached"
        self._log_window.clear()

    def _run_command(self, event):
        assert hasattr(self, '_command_window'), "command window not attached"
        command = self._command_window.get_command()
        command = command.strip()
        self._log(command)

        if command == 'clear':
            self._clear_log()
